## class 2.0

import logging
from typing import Union, Any

log = logging.getLogger(__name__)


class Orcid:
    """Provide any ORCID string and normalize it to the official format
    class attributes:
        RAISE_EXCEPTION_ON_UNPARSABLE_ORCID_STRING: bool; If set to True, raise an exception for strings that are not recognizable as ORCIDs. Otherwise just return RETURN_VAL_ON_INVALID
        RETURN_VAL_ON_INVALID: Any; If RAISE_EXCEPTION_ON_INVALID_STRING is False, this will be returned instead of raising an exception
    """

    RAISE_EXCEPTION_ON_UNPARSABLE_ORCID_STRING: bool = True
    RETURN_VAL_ON_UNPARSABLE: Any = None

    ORCID_URL: str = "https://orcid.org/"

    def __init__(self, id_: Union[str, int]):
        self.raw_input = id_
        self._raw_urn_values = self._extract_raw_urn_values(self.raw_input)
        self.urn = self._format_raw_urn_values(self._raw_urn_values)

    @property
    def uri(self) -> str:
        return (
            f"{self.ORCID_URL}{self.urn}"
            if self.urn != self.RETURN_VAL_ON_UNPARSABLE
            else self.RETURN_VAL_ON_UNPARSABLE
        )

    def is_valid(self) -> bool:
        return self._checksum_test()

    def _extract_raw_urn_values(self, input):
        msg = None
        if type(input) not in [str, int]:
            msg = f"Orcid not parsable. Expected [str,int] got {type(input)}"

        # extracted ocrid by removing everything but digits and "x"
        id_only = "".join(
            filter(lambda x: x.isdigit() or x.lower() == "x", str(input))
        ).upper()

        # check if extracted ORCID is not empty
        if id_only == "":
            msg = f"Orcid not parsable. '{input}' contains no numbers."

        # check if extracted ORCID contains x and if yes that "x" is only at the end of the string
        if (
            not msg
            and "X" in id_only
            and (id_only.count("X") > 1 or not id_only.endswith("X"))
        ):
            msg = f"Orcid malformed. '{input}' contains multiple 'X' (count:{id_only.count('X')}) or 'X' not only at the end"

        # check for healthy length
        if not msg and len(id_only) > 16:
            msg = f"Orcid malformed. '{input}' contains to many digits (Max 16)."

        if msg and self.RAISE_EXCEPTION_ON_UNPARSABLE_ORCID_STRING:
            raise ValueError(msg)
        elif msg:
            logging.debug(msg)
            return self.RETURN_VAL_ON_UNPARSABLE
        return id_only

    def _checksum_test(self) -> bool:

        ###
        #   For information about how and why the checksum is calculated see https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier
        ###
        total = 0

        for char in self.urn[:-1]:
            if char.isdigit():
                total = (total + int(char)) * 2

        remainder = total % 11
        result = (12 - remainder) % 11

        if str(result) == self.urn[-1] or (self.urn[-1] == "X" and result == 10):
            return True
        else:
            return False

    def _format_raw_urn_values(self, raw_urn_values: str) -> str:
        if raw_urn_values == self.RETURN_VAL_ON_UNPARSABLE:
            return self.RETURN_VAL_ON_UNPARSABLE
        raw_urn_values = raw_urn_values.zfill(16)
        formated_urn = (
            raw_urn_values[0:4]
            + "-"
            + raw_urn_values[4:8]
            + "-"
            + raw_urn_values[8:12]
            + "-"
            + raw_urn_values[12:16]
        )
        return formated_urn

    def __str__(self):
        return self.uri
