import pathlib
from bsdd import Client
from sys import exit
import csv

IFC4X3_URI = "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3"
BDNS_REGISTER = pathlib.Path(__file__).parent.parent / "BDNS_Abbreviations_Register.csv"

def read_csv(path: pathlib.Path) -> list[list]:
    """Read a CSV file and return its content as a list of lists."""
    data = list(csv.reader(path.read_text().split("\n")))
    if data[-1] == []:
        data = data[:-1]
    return data


def get_ifc_classes(client):
    def get_batch(i):
        return client.get_classes(
            IFC4X3_URI,
            use_nested_classes=False,
            class_type="Class",
            offset=i[0],
            limit=i[1],
        )["classes"]

    ifc_classes = {}
    for i in [(0, 1000), (1000, 2000)]:  # 1418 classes in total. 1000 max request limit
        ifc_classes = ifc_classes | {x["code"]: x for x in get_batch(i)}
    return ifc_classes


# get all valid ifc4_3 classes from the bsdd client
client = Client()
di_ifc_classes = get_ifc_classes(client)
li_ifc_classes = list(di_ifc_classes.keys())

# get all ifc4_3 classes from the BDNS register
abbreviations = read_csv(BDNS_REGISTER)
ifc_classes_bdns = [x[-3].replace("NOTDEFINED", "").replace("USERDEFINED", "") for x in abbreviations[1:] if x[-3] != ""]

invalid_ifc_classes = [x for x in ifc_classes_bdns if x not in li_ifc_classes]


assert len(invalid_ifc_classes) == 0, f"Invalid IFC classes found: {invalid_ifc_classes}"


if len(invalid_ifc_classes) > 0:
    print("Invalid IFC classes found:")
    print(invalid_ifc_classes)
    exit(1)
else:
    print("All IFC classes in 'ifc4_3' column are valid.")
