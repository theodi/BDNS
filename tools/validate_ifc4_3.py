import pandas as pd
import pathlib
from bsdd import Client

IFC4X3_URI = "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3"
BDNS_REGISTER = pathlib.Path(__file__).parent.parent / "BDNS_Abbreviations_Register.csv"

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

client = Client()
di_ifc_classes = get_ifc_classes(client)
li_ifc_classes = list(di_ifc_classes.keys())
df_bdns = pd.read_csv(BDNS_REGISTER)

# Validate that all values in the 'ifc4_3' column are in li_ifc_classes
invalid_ifc_classes = df_bdns[~df_bdns["ifc4_3"].isin(li_ifc_classes)]

assert invalid_ifc_classes.empty, f"Invalid IFC classes found: {invalid_ifc_classes['ifc4_3'].tolist()}"
print("All IFC classes in 'ifc4_3' column are valid.")
