import datetime
import logging
from typing import Any, NamedTuple

from dateutil.parser import parse
from sqlite_utils.db import Database, Table

from .justice_model import Justice
from .justice_name import OpinionWriterName


class JusticeDetail(NamedTuple):
    justice_id: int | None = None
    raw_ponente: str | None = None
    designation: str | None = "J."
    per_curiam: bool = False


class CandidateJustice(NamedTuple):
    db: Database
    text: str | None = None
    date_str: str | None = None

    @property
    def valid_date(self) -> datetime.date | None:
        if not self.date_str:
            return None
        try:
            return parse(self.date_str).date()
        except Exception:
            return None

    @property
    def src(self):
        return OpinionWriterName.extract(self.text)

    @property
    def candidate(self) -> str | None:
        return self.src and self.src.writer

    @property
    def table(self) -> Table:
        res = self.db[Justice.__tablename__]
        if isinstance(res, Table):
            return res
        raise Exception("Not a valid table.")

    @property
    def rows(self) -> list[dict]:
        """When selecting a ponente or voting members, create a candidate list of
        justices based on the `valid_date`.

        Examples:
            >>> import yaml
            >>> from pathlib import Path
            >>> from sqlpyd import Connection
            >>> from corpus_judge import JUSTICE_FILE
            >>> c = Connection(DatabasePath="test.db")
            >>> c.path_to_db.unlink(missing_ok=True) # tear down
            >>> tbl = c.create_table(Justice)
            >>> res = c.add_records(Justice, yaml.safe_load(JUSTICE_FILE.read_bytes()))
            >>> search = CandidateJustice(db=c.db, date_str='Dec. 1, 1995')
            >>> print(search.rows) # since start date is greater than target date, record is included
            [{'id': 137, 'surname': 'panganiban', 'alias': None, 'start_term': '1995-10-05', 'inactive_date': '2006-12-06', 'chief_date': '2005-12-20'}, {'id': 136, 'surname': 'hermosisima', 'alias': 'hermosisima jr.', 'start_term': '1995-01-10', 'inactive_date': '1997-10-18', 'chief_date': None}, {'id': 135, 'surname': 'francisco', 'alias': None, 'start_term': '1995-01-05', 'inactive_date': '1998-02-13', 'chief_date': None}, {'id': 134, 'surname': 'mendoza', 'alias': None, 'start_term': '1994-06-07', 'inactive_date': '2003-04-05', 'chief_date': None}, {'id': 133, 'surname': 'kapunan', 'alias': None, 'start_term': '1994-01-05', 'inactive_date': '2002-08-12', 'chief_date': None}, {'id': 132, 'surname': 'vitug', 'alias': None, 'start_term': '1993-06-28', 'inactive_date': '2004-07-15', 'chief_date': None}, {'id': 131, 'surname': 'puno', 'alias': None, 'start_term': '1993-06-28', 'inactive_date': '2010-05-17', 'chief_date': '2007-12-08'}, {'id': 128, 'surname': 'melo', 'alias': None, 'start_term': '1992-08-10', 'inactive_date': '2002-05-30', 'chief_date': None}, {'id': 127, 'surname': 'bellosillo', 'alias': None, 'start_term': '1992-03-03', 'inactive_date': '2003-11-13', 'chief_date': None}, {'id': 125, 'surname': 'romero', 'alias': None, 'start_term': '1991-10-21', 'inactive_date': '1999-08-01', 'chief_date': None}, {'id': 124, 'surname': 'davide', 'alias': 'davide jr.', 'start_term': '1991-01-24', 'inactive_date': '2005-12-20', 'chief_date': '1998-11-30'}, {'id': 123, 'surname': 'regalado', 'alias': None, 'start_term': '1988-07-29', 'inactive_date': '1998-10-13', 'chief_date': None}, {'id': 116, 'surname': 'padilla', 'alias': None, 'start_term': '1987-01-12', 'inactive_date': '1997-08-22', 'chief_date': None}, {'id': 115, 'surname': 'feliciano', 'alias': None, 'start_term': '1986-08-08', 'inactive_date': '1995-12-13', 'chief_date': None}, {'id': 112, 'surname': 'narvasa', 'alias': None, 'start_term': '1986-04-10', 'inactive_date': '1998-11-30', 'chief_date': '1991-12-08'}]
            >>> c.path_to_db.unlink() # tear down

        Returns:
            list[dict]: Filtered list of justices
        """  # noqa: E501
        if not self.valid_date:
            return []
        criteria = "inactive_date > :date and :date > start_term"
        params = {"date": self.valid_date.isoformat()}
        results = self.table.rows_where(
            where=criteria,
            where_args=params,
            select=(
                "id, lower(last_name) surname, alias, start_term,"
                " inactive_date, chief_date"
            ),
            order_by="start_term desc",
        )
        return list(results)

    @property
    def choice(self) -> dict | None:
        """Based on `@rows`, match the cleaned_name to either the alias
        of the justice or the justice's last name; on match, determine whether the
        designation should be 'C.J.' or 'J.'

        Examples:
            >>> import yaml
            >>> from pathlib import Path
            >>> from sqlpyd import Connection
            >>> p = Path(__file__).parent / "sc.yaml"
            >>> c = Connection(DatabasePath="test.db")
            >>> c.path_to_db.unlink(missing_ok=True) # tear down
            >>> tbl = c.create_table(Justice)
            >>> res = c.add_records(Justice, yaml.safe_load(p.read_bytes()))
            >>> search = CandidateJustice(db=c.db, text='Panganiban, Acting Cj', date_str='Dec. 1, 1995')
            >>> print(search.choice) # note variance in text designation as acting CJ. vs. J.
            {'id': 137, 'surname': 'Panganiban', 'start_term': '1995-10-05', 'inactive_date': '2006-12-06', 'chief_date': '2005-12-20', 'designation': 'J.'}
            >>> # Note that the raw information above contains 'Acting Cj' and thus the designation is only 'J.' At present we only track 'C.J.' and 'J.' titles.
            >>> # With a different date, we can get the 'C.J.' designation.:
            >>> search_cj = CandidateJustice(db=c.db, text='Panganiban', date_str='2006-03-30')
            >>> print(search_cj.choice) # note variance in text designation as acting CJ. vs. J.
            {'id': 137, 'surname': 'Panganiban', 'start_term': '1995-10-05', 'inactive_date': '2006-12-06', 'chief_date': '2005-12-20', 'designation': 'C.J.'}
            >>> c.path_to_db.unlink() # tear down
        """  # noqa: E501
        candidate_options = []
        if not self.valid_date:
            return None

        if self.text:
            # Special rule for duplicate names
            if "Lopez" in self.text:
                if "jhosep" in self.text.lower():
                    for candidate in self.rows:
                        if int(candidate["id"]) == 190:
                            candidate_options.append(candidate)
                elif "mario" in self.text.lower():
                    for candidate in self.rows:
                        if int(candidate["id"]) == 185:
                            candidate_options.append(candidate)

        # only proceed to add more options if special rule not met
        if not candidate_options:
            if not self.candidate:
                return None

            for candidate in self.rows:
                if candidate["alias"] and candidate["alias"] == self.candidate:
                    candidate_options.append(candidate)
                    continue
                elif candidate["surname"] == self.candidate:
                    candidate_options.append(candidate)
                    continue

        if candidate_options:
            if len(candidate_options) == 1:
                res = candidate_options[0]
                res.pop("alias")
                res["surname"] = res["surname"].title()
                res["designation"] = "J."
                if chief_date := res.get("chief_date"):
                    s = parse(chief_date).date()
                    e = parse(res["inactive_date"]).date()
                    if s < self.valid_date < e:
                        res["designation"] = "C.J."
                return res
            else:
                msg = f"Too many {candidate_options=} for {self.candidate=} on {self.valid_date=}. Consider manual intervention."  # noqa: E501
                logging.error(msg)

        return None

    @property
    def detail(self) -> JusticeDetail | None:
        """Get object to match fields directly

        Examples:
            >>> import yaml
            >>> from pathlib import Path
            >>> from sqlpyd import Connection
            >>> from corpus_judge import JUSTICE_FILE
            >>> c = Connection(DatabasePath="test.db")
            >>> c.path_to_db.unlink(missing_ok=True) # tear down
            >>> tbl = c.create_table(Justice)
            >>> res = c.add_records(Justice, yaml.safe_load(JUSTICE_FILE.read_bytes()))
            >>> search = CandidateJustice(db=c.db, text='Panganiban, Acting Cj', date_str='Dec. 1, 1995')
            >>> print(search.detail)
            JusticeDetail(justice_id=137, raw_ponente='Panganiban', designation='J.', per_curiam=False)
            >>> c.path_to_db.unlink() # tear down

        Returns:
            JusticeDetail | None: Will subsequently be used in DecisionRow in a third-party library.
        """  # noqa: E501
        if not self.src:
            return None

        if self.src.per_curiam:
            return JusticeDetail(
                justice_id=None,
                raw_ponente=None,
                designation=None,
                per_curiam=True,
            )
        elif self.choice and self.choice.get("id", None):
            digit_id = int(self.choice["id"])
            return JusticeDetail(
                justice_id=digit_id,
                raw_ponente=self.choice["surname"],
                designation=self.choice["designation"],
                per_curiam=False,
            )
        return None

    @property
    def id(self) -> int | None:
        return self.detail.justice_id if self.detail else None

    @property
    def per_curiam(self) -> bool:
        return self.detail.per_curiam if self.detail else False

    @property
    def raw_ponente(self) -> str | None:
        return self.detail.raw_ponente if self.detail else None

    @property
    def ponencia(self) -> dict[str, Any]:
        """Produces a dict of partial fields that include the following keys:

        1. `justice_id`: int
        2. `raw_ponente`: str
        3. `per_curiam`: bool
        """
        return {
            "justice_id": self.id,
            "raw_ponente": self.raw_ponente,
            "per_curiam": self.per_curiam,
        }
