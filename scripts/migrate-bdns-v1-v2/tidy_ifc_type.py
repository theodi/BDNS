import pandas as pd
import pathlib
from bsdd import Client

IFC4X3_URI = "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3"
BDNS_REGISTER = pathlib.Path(__file__).parent.parent.parent / "BDNS_Abbreviations_Register.csv"

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


def remove_invalid_type_for_abbreviation(abbreviation, df_bdns):
    index = df_bdns[df_bdns["asset_abbreviation"] == abbreviation].index
    df_bdns.loc[index, "ifc_type"] = ""
    return df_bdns

# PDB: IfcAlarmTWOPOSITION does not exist
df_bdns = remove_invalid_type_for_abbreviation("PDB", df_bdns)


# the following classes do not exist in IFC 4.3
# APSW: IfcSwitchingDevicePRESSURESENSOR
df_bdns = remove_invalid_type_for_abbreviation("APSW", df_bdns)

# DEWSW: IfcSwitchingDeviceHUMIDISTAT
df_bdns = remove_invalid_type_for_abbreviation("DEWSW", df_bdns)

# DPSW: IfcSwitchingDevicePRESSURESENSOR
df_bdns = remove_invalid_type_for_abbreviation("DPSW", df_bdns)

# SPSW: IfcSwitchingDevicePRESSURESENSOR
df_bdns = remove_invalid_type_for_abbreviation("SPSW", df_bdns)

# ^ I think there was confusion about whether to use `IfcSensor` or `IfcSwitchingDevice` for these classes ^
# we will use `IfcSwitchingDevice` 

df_bdns["ifc_type"] = df_bdns["ifc_type"].fillna("")
df_bdns["ifc4_3"] = df_bdns["ifc_class"] + df_bdns["ifc_type"]
# check all IFC classes are in IFC 4.3. NOTE. the above amendments were introduced to ensure this
not_ifc4_3 = {
    row.asset_abbreviation: row.ifc4_3
    for _, row in df_bdns.iterrows()
    if row.ifc4_3 not in li_ifc_classes
}
assert len(not_ifc4_3) == 0, f"Classes not in IFC 4.3: {not_ifc4_3}"

del df_bdns["ifc4_3"]
df_bdns.to_csv(BDNS_REGISTER, index=False, encoding="utf-8")
print("done")