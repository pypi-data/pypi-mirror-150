import os, sys

if __name__ == "__main__":
    # Wir holen uns den aktuellen pfads in dem test.py liegt
    SCRIPT_DIR = os.path.dirname(
        os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
    )
    # Extrahieren uns den darüberliegenden ordner in dem unser module liegt
    SCRIPT_DIR = os.path.join(SCRIPT_DIR, "..")
    # wir fügen diesen order sys.path als directory hinzu
    sys.path.insert(0, os.path.normpath(SCRIPT_DIR))

from OrcidNormalizer import Orcid

ids = [
    ("https://orcid.org/1-5000-0074", "valid"),
    ("http://orcid.org/0003 2890 3781", "valid"),
    (218250097, "valid"),
    ("https://orcid.org/1-5000-007X", "invalid"),
    ("http://pete123@mail.net", "invalid"),
    (3211198634, "invalid"),
    ("theresa@mymail.com", "unparsable"),
]

Orcid.RAISE_EXCEPTION_ON_UNPARSABLE_ORCID_STRING = False
Orcid.RETURN_VAL_ON_UNPARSABLE = "invalid"
for _id, expected_result in ids:

    print(f"\n---input: {type(_id)} '{_id}'")
    orcid = Orcid(_id)
    is_valid = orcid.is_valid()
    print("is valid: ", is_valid)
    print("normaized urn: ", orcid.urn)
    print("normaized uri: ", orcid.uri)
    if expected_result == "valid":
        assert is_valid and orcid.urn != Orcid.RETURN_VAL_ON_UNPARSABLE
    elif expected_result == "invalid":
        assert not is_valid and orcid.urn != Orcid.RETURN_VAL_ON_UNPARSABLE
    elif expected_result == "unparsable":
        assert not is_valid and orcid.urn == Orcid.RETURN_VAL_ON_UNPARSABLE
