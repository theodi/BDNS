import pathlib
import csv
import re
import itertools

BDNS_REGISTER = pathlib.Path(__file__).parent.parent.parent / "BDNS_Abbreviations_Register.csv"

def read_csv(path: pathlib.Path) -> list[list]:
    """Read a CSV file and return its content as a list of lists."""
    data = list(csv.reader(path.read_text().split("\n")))
    if data[-1] == []:
        data = data[:-1]
    return data

def write_csv(path: pathlib.Path, data: list[list]) -> None:
    """Write a list of lists to a CSV file."""
    with path.open("w", newline="") as f:
        csv.writer(f).writerows(data)

abbreviations = read_csv(BDNS_REGISTER)
can_be_connected = {x[0]: x[1] for x in read_csv(pathlib.Path(__file__).parent / "add-can-be-connected.csv")[1:]}

for k,v in can_be_connected.items():
    for n, x in enumerate(abbreviations):
        if x[1] == k:
            abbreviations[n][2] = v
            break

write_csv(BDNS_REGISTER, abbreviations)
print("done")