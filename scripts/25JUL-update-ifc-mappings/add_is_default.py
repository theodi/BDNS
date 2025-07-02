import pathlib
import csv
import re

BDNS_REGISTER = pathlib.Path(__file__).parent.parent.parent / "BDNS_Abbreviations_Register.csv"


def read_csv(path: pathlib.Path) -> list[list]:
    """Read a CSV file and return its content as a list of lists."""
    return list(csv.reader(path.read_text().split("\n")))

def write_csv(path: pathlib.Path, data: list[list]) -> None:
    """Write a list of lists to a CSV file."""
    with path.open("w", newline="") as f:
        csv.writer(f).writerows(data)

def ifc_strip_enum(ifc_class: str) -> str:
    return re.sub(r"([A-Z0-9_]+_?)$", "", ifc_class)


def ifc_class_is_enum(ifc_class: str) -> bool:
    return ifc_strip_enum(ifc_class) != ifc_class

abbreviations = read_csv(BDNS_REGISTER)
abbreviations = [[*x, *["is_ifc_default"]] if n == 0 else [*x, *[0]] for n, x in enumerate(abbreviations)]

write_csv(BDNS_REGISTER, abbreviations)