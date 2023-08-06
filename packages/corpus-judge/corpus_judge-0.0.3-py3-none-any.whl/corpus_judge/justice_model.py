import datetime
from pathlib import Path

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta as rd
from pydantic import Field, validator
from sqlpyd import IndividualBio

MAX_JUSTICE_AGE = 70  # 1987 Constitution
JUSTICE_FILE = Path(__file__).parent / "sc.yaml"


class Bio(IndividualBio):
    @classmethod
    def from_dict(cls, data: dict):
        sfx = data.pop("Suffix")
        return cls(
            first_name=data.pop("First Name"),
            last_name=data.pop("Last Name"),
            suffix=None if sfx == "" else sfx,
            full_name=data.pop("Justice"),
            gender=data.pop("Gender"),
            nick_name=None,
        )


class Justice(Bio):
    """
    # Justice

    Field | Type | Description
    --:|:--|:--
    id |int | Unique identifier of the Justice based on appointment roster
    full_name |str | First + last + suffix
    first_name |str | -
    last_name |str | -
    suffix |str | e.g. Jr., Sr., III, etc.
    nick_name |str | -
    gender |str | -
    alias |str | Other names
    start_term |str | Time justice appointed
    end_term |str | Time justice
    chief_date |str | Date appointed as Chief Justice (optional)
    birth_date |str | Date of birth
    retire_date |str | Based on the Birth Date, if it exists, it is the maximum term of service allowed by law.
    inactive_date |str | Which date is earliest inactive date of the Justice, the retire date is set automatically but it is not guaranteed to to be the actual inactive date. So the inactive date is either that specified in the `end_term` or the `retire_date`, whichever is earlier.

    Examples:
        >>> # See database
        >>> from sqlpyd import Connection
        >>> from sqlite_utils.db import Table
        >>> c = Connection(DatabasePath="test.db")
        >>> c.path_to_db.unlink(missing_ok=True) # tear down
        >>> table = c.create_table(Justice)
        >>> isinstance(table, Table)
        True
        >>> # See local file
        >>> JUSTICE_FILE.exists()
        True
        >>> # Can add all pydantic validated records from the local copy of justices to the database.
        >>> import yaml
        >>> res = c.add_records(Justice, yaml.safe_load(JUSTICE_FILE.read_bytes()))
        >>> len(list(table.rows))
        194
        >>> c.path_to_db.unlink() # tear down

    The list of justices from the sc.yaml file are parsed through this model prior to being inserted
    into the database.
    """  # noqa: E501

    __prefix__ = "sc"
    __tablename__ = "justices"
    __indexes__ = [
        ["last_name", "alias", "start_term", "inactive_date"],
        ["start_term", "inactive_date"],
        ["last_name", "alias"],
    ]

    id: int = Field(
        ...,
        title="Justice ID Identifier",
        description=(
            "Starting from 1, the integer represents the order of appointment"
            " to the Supreme Court."
        ),
        ge=1,
        lt=1000,
        col=int,
    )
    alias: str | None = Field(
        None,
        title="Alias",
        description="Means of matching ponente and voting strings to the justice id.",
        col=str,
        index=True,
    )
    start_term: datetime.date | None = Field(
        None,
        title="Start Term",
        description="Date of appointment.",
        col=datetime.date,
        index=True,
    )
    end_term: datetime.date | None = Field(
        None,
        title="End Term",
        description="Date of termination.",
        col=datetime.date,
        index=True,
    )
    chief_date: datetime.date | None = Field(
        None,
        title="Date Appointed As Chief Justice",
        description=(
            "When appointed, the extension title of the justice changes from"
            " 'J.' to 'C.J'. for cases that are decided after the date of"
            " appointment but before the date of retirement."
        ),
        col=datetime.date,
        index=True,
    )
    birth_date: datetime.date | None = Field(
        None,
        title="Date of Birth",
        description=(
            "The Birth Date is used to determine the retirement age of the"
            " justice. Under the 1987 constitution, this is"
            f" {MAX_JUSTICE_AGE}. There are missing dates: see Jose Generoso"
            " 41, Grant Trent 14, Fisher 19, Moir 20."
        ),
        col=datetime.date,
        index=True,
    )
    retire_date: datetime.date | None = Field(
        None,
        title="Mandatory Retirement Date",
        description=(
            "Based on the Birth Date, if it exists, it is the maximum term of"
            " service allowed by law."
        ),
        col=datetime.date,
        index=True,
    )
    inactive_date: datetime.date | None = Field(
        None,
        title="Date",
        description=(
            "Which date is earliest inactive date of the Justice, the retire"
            " date is set automatically but it is not guaranteed to to be the"
            " actual inactive date. So the inactive date is either that"
            " specified in the `end_term` or the `retire_date`, whichever is"
            " earlier."
        ),
        col=datetime.date,
        index=True,
    )

    @validator("retire_date")
    def retire_date_70_years(cls, v, values):
        if v and values["birth_date"]:
            if values["birth_date"] + rd(years=MAX_JUSTICE_AGE) != v:
                raise ValueError("Must be 70 years from birth date.")
        return v

    class Config:
        use_enum_values = True

    @classmethod
    def from_data(cls, data: dict):
        def extract_date(text: str | None) -> datetime.date | None:
            return parse(text).date() if text else None

        bio = Bio.from_dict(data)

        # Not all justices have/need aliases; default needed
        alias = data.pop("Alias", None)
        if not alias:
            if bio.last_name and bio.suffix:
                alias = f"{bio.last_name} {bio.suffix}".lower()

        retire_date = None
        if dob := extract_date(data.pop("Born")):
            retire_date = dob + rd(years=MAX_JUSTICE_AGE)

        # retire_date = latest date allowed; but if end_date present, use this
        inactive_date = retire_date
        if end_date := extract_date(data.pop("End of term")):
            inactive_date = end_date or retire_date

        return cls(
            **bio.dict(exclude_none=True),
            id=data.pop("#"),
            alias=alias,
            birth_date=dob,
            start_term=extract_date(data.pop("Start of term")),
            end_term=end_date,
            chief_date=extract_date(data.pop("Appointed chief")),
            retire_date=retire_date,
            inactive_date=inactive_date,
        )
