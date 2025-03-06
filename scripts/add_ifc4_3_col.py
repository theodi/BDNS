import pandas as pd
import pathlib

BDNS_REGISTER = pathlib.Path(__file__).parent.parent / "BDNS_Abbreviations_Register.csv"

df_bdns = pd.read_csv(BDNS_REGISTER)

df_bdns["ifc_type"] = df_bdns["ifc_type"].fillna("")
df_bdns["ifc4_3"] = df_bdns["ifc_class"] + df_bdns["ifc_type"]

cols = [
    "asset_description",
    "asset_abbreviation",
    "can_be_connected", # MOVE: as this is a "core" bdns field not a mapping
    "dbo_entity_type",
    # "ifc_class",  # DELETE
    # "ifc_type", # DELETE
    "ifc4_3", # ADD
]

df_bdns[cols].to_csv(BDNS_REGISTER, index=False, encoding="utf-8")
print("done")
