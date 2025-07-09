import pathlib
import csv

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
for n, x in enumerate(abbreviations):
    if n>0:
        try:
            abbreviations[n][2] = x[2].replace("1.0", "1").replace("0.0", "0")
        except Exception as e:
            print(x[1], x[2])



write_csv(BDNS_REGISTER, abbreviations)    