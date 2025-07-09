import pathlib
import csv
import re
from sys import exit

BDNS_REGISTER = pathlib.Path(__file__).parent.parent / "BDNS_Abbreviations_Register.csv"


def ifc_strip_enum(ifc_class: str) -> str:
    return re.sub(r"([A-Z0-9_]+_?)$", "", ifc_class)


def ifc_class_is_enum(ifc_class: str) -> bool:
    return ifc_strip_enum(ifc_class) != ifc_class

def read_csv(path: pathlib.Path) -> list[list]:
    """Read a CSV file and return its content as a list of lists."""
    data = list(csv.reader(path.read_text().split("\n")))
    if data[-1] == []:
        data = data[:-1]
    return data

abbreviations = read_csv(BDNS_REGISTER)
defaults = [x for x in abbreviations[1:] if x[-1] == "1"]
default_abbreviations = [x[1] for x in defaults]
duplicates = [i for i in set(default_abbreviations) if default_abbreviations.count(i) > 1]
unique_defaults = list(set(default_abbreviations))


assert len(duplicates) == 0, f"There are duplicate default mappings in BDNS Abbreviations Register: {duplicates}"
if len(duplicates) == 0:
    print("All default ifc4_3 is_default_ifc mappings in BDNS Abbreviations Register are unique.")


# TODO: check core classes are unique
ifc_4_3_mappings = [x[-2] for x in abbreviations[1:] if x[-2] != ""]
ifc_4_3_core = [x for x in ifc_4_3_mappings if not ifc_class_is_enum(x)]
duplicate_ifc_4_3_core = [i for i in set(default_abbreviations) if default_abbreviations.count(i) > 1]
assert len(duplicate_ifc_4_3_core) == 0, f"Core ifc mappings are not unique: {duplicate_ifc_4_3_core}"
if len(duplicate_ifc_4_3_core) == 0:
    print("All default ifc4_3 mappings that do not specify and enum are unique.")
else:
    exit(1)