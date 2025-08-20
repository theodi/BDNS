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

is_ifc_default_index = abbreviations[0].index("is_ifc_default") 
ifc4_3_index = abbreviations[0].index("ifc4_3")
asset_abbreviation_index = abbreviations[0].index("asset_abbreviation")

defaults = [x for x in abbreviations[1:] if x[is_ifc_default_index] == "1"]
default_abbreviations = [x[asset_abbreviation_index] for x in defaults]
duplicates = [i for i in set(default_abbreviations) if default_abbreviations.count(i) > 1]
unique_defaults = list(set(default_abbreviations))


assert len(default_abbreviations) == len(unique_defaults), f"There are duplicate default mappings in BDNS Abbreviations Register: {duplicates}"
if len(default_abbreviations) == len(unique_defaults):
    print("All default ifc4_3 is_default_ifc mappings in BDNS Abbreviations Register are unique.")


# TODO: check core classes are unique
ifc_4_3_mappings = [x[ifc4_3_index] for x in abbreviations[1:] if x[ifc4_3_index] != ""]
ifc_4_3_core = [x for x in ifc_4_3_mappings if not ifc_class_is_enum(x)]

unique_ifc_core = list(set(ifc_4_3_core))

count_duplicate_ifc_core_mappings = dict(sorted(
    ((x, ifc_4_3_core.count(x)) for x in set(ifc_4_3_core)),
    key=lambda item: item[1],
    reverse=True
))

for k, v in count_duplicate_ifc_core_mappings.items():
    if v > 1:
        print(f"{k} appears {v} times.")

# duplicate_ifc_4_3_core = [i for i in set(default_abbreviations) if default_abbreviations.count(i) > 1]
# assert len(duplicate_ifc_4_3_core) == 0, f"Core ifc mappings are not unique: {duplicate_ifc_4_3_core}"
if len(default_abbreviations) == len(unique_defaults):
    print("---end---")
else:
    exit(1)