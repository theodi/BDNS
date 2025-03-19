import pandas as pd
import pathlib
from bsdd import Client

IFC4X3_URI = "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3"
BDNS_REGISTER = pathlib.Path(__file__).parent.parent / "BDNS_Abbreviations_Register.csv"
BDNS_ALEX_UPDATE = pathlib.Path(__file__).parent / "BDNS to IFC.csv"


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
df_alex = pd.read_csv(BDNS_ALEX_UPDATE)

# to match the formatting of the updated BDNS file wrt to Types and NOTDEFINED etc. I'll apply the same
# changes I've made to the main BDNS file to the Alex update file

df_alex["ifc4_3_update"] = df_alex["IFC4.3"]
df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].str.replace("NOTDEFINED", "")
df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].str.replace("USERDEFINED", "")
df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].str.strip()
df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].str.replace("Type", "")
df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].str.replace("Enum", "")
df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].str.replace("ifc", "Ifc")
df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].str.replace("Ifcvalve", "IfcValve")

df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].str.replace(
    "IfcElectricDistributionBoard", "IfcDistributionBoard"
)
df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].str.replace(".", "")
df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].str.replace(
    "NOTEDEFINED", ""
)  # fix typo
df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].str.replace(
    "NOT DEFINED", ""
)  # fix typo
df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].str.replace(
    "IfcSwitchingDevicePRESSURESENSOR", "IfcSwitchingDevice"
)  # fix error
df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].str.replace(
    "IfcSwitchingDeviceHUMIDISTAT", "IfcSwitchingDevice"
)  # fix error


def remove_duplicates(x: str):
    if "," in x:
        li = list(set(x.split(",")))
        if len(li) > 1:
            x = ",".join(li)
        elif len(li) == 1:
            x = li[0]
        else:
            pass
    return x


df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].fillna("")
df_alex["ifc4_3_update"] = df_alex["ifc4_3_update"].apply(remove_duplicates)

di_bdns = {
    f"{row.asset_abbreviation} | {row.asset_description}": row.ifc4_3
    for _, row in df_bdns.iterrows()
}
di_alex = {
    f"{row.asset_abbreviation} | {row.asset_description}": row.ifc4_3_update
    for _, row in df_alex.iterrows()
}

di_diff = {
    k: {"alex": v, "bdns": di_bdns.get(k)}
    for k, v in di_alex.items()
    if di_bdns.get(k) != v
}
di_diff = {k: v for k, v in di_diff.items() if v["alex"] != ""}
# ^ this gets the dif

di_diff = {
    k: v for k, v in di_diff.items() if v["bdns"] is not None
}  # RTE was changed... for exampel

changes = [x.split(" | ")[0] for x in list(di_diff.keys())]

# I manually reviewed the diff and think the following are acceptable and non-contentious
accept = [
    # "ACT",
    # "AT",
    # "ROOM",
    "CAFTRK",
    "ACCH",
    "WCCH",
    "COIL",
    "DXC",
    "PHC",
    "RHC",
    "RAC",
    "CKROT",
    "COAXCA",
    # "DCA",  # could be copper
    # "CA",
    # "FCA",
    "FDR",
    # "ECG", # multiple... needs discussion
    # "ADS",
    # "AS",
    # "CTFS",
    "FSCPL",
    "FSCWL",
    "FSHCPL",
    "FSHCWL",
    "FSHPL",
    "FSHWL",
    "FSIWL",
    "FSSWL",
    "KSTCH",
    "KTBL",
    "HIU",
    # "TR",
    "EBA",
    "ERO",
    "ETA",
    # "APSW", - switch or sensor
    # "DEWSW", - switch or sensor
    # "DPSW", - switch or sensor
    # "SPSW", - switch or sensor
    "CDWRT",
    "CHDU",
    "DPOT",
    "EMWC",
    # "WD", # multiple... needs discussion
]

needs_review = [x for x in changes if x not in accept]
di_accept = {k.split(" | ")[0]: v for k, v in di_diff.items() if k.split(" | ")[0] in accept}


for k, v in di_accept.items():
    index = df_bdns.asset_abbreviation == k
    df_bdns.loc[index, "ifc4_3"] = v["alex"]


df_bdns.to_csv(BDNS_REGISTER, index=False, encoding="utf-8")
li_needs_review = [{"asset" :k} | v for k, v in di_diff.items() if k.split(" | ")[0] in needs_review]
df_needs_review = pd.DataFrame(li_needs_review)
df_needs_review.to_csv(pathlib.Path(__file__).parent / "needs_review.csv", index=False, encoding="utf-8")

