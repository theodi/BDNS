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

df_bdns["ifc_class"] = df_bdns[
    "ifc_class"
].str.strip()  # remove leading and trailing whitespaces
df_bdns["ifc_class"] = df_bdns["ifc_class"].str.replace(
    "Type", ""
)  # remove Type from ifc_class
df_bdns["ifc_class"] = df_bdns["ifc_class"].str.replace(
    "Enum", ""
)  # remove Enum from ifc_class
df_bdns["ifc_class"] = df_bdns["ifc_class"].str.replace("ifc", "Ifc")
df_bdns["ifc_class"] = df_bdns["ifc_class"].str.replace("Ifcvalve", "IfcValve")

df_bdns["ifc_class"] = df_bdns["ifc_class"].str.replace(
    "IfcElectricDistributionBoard", "IfcDistributionBoard"
)
# see `IfcElectricDistributionBoard` deprecation notice ^
# https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcElectricDistributionBoard.htm


# check all IFC classes are in IFC 4.3
not_ifc4_3 = {
    row.asset_abbreviation: row.ifc_class
    for _, row in df_bdns.iterrows()
    if row.ifc_class not in li_ifc_classes
}
assert len(not_ifc4_3) == 0, f"Classes not in IFC 4.3: {not_ifc4_3}"


df_bdns.to_csv(BDNS_REGISTER, index=False, encoding="utf-8")
print("done")
