import pandas as pd
import pathlib

BDNS_REGISTER = pathlib.Path(__file__).parent.parent.parent / "BDNS_Abbreviations_Register.csv"

df_bdns = pd.read_csv(BDNS_REGISTER)

# NOTE. in IFC 4.3 on BSDD there are no classes for `NOTDEFINED` or `USERDEFINED` so ignoring these
df_bdns["ifc_type"] = df_bdns["ifc_type"].str.replace("NOTDEFINED", "")
df_bdns["ifc_type"] = df_bdns["ifc_type"].str.replace("USERDEFINED", "")
df_bdns["ifc_type"] = df_bdns["ifc_type"].str.replace("NOTEDEFINED", "") # fix typo
df_bdns["ifc_type"] = df_bdns["ifc_type"].str.replace("NOT DEFINED", "") # fix typo

df_bdns.to_csv(BDNS_REGISTER, index=False, encoding="utf-8")
print("done")