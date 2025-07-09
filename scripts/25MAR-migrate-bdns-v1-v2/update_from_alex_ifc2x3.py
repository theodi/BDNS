import pandas as pd
import pathlib

BDNS_REGISTER = pathlib.Path(__file__).parent.parent.parent / "BDNS_Abbreviations_Register.csv"
BDNS_ALEX_UPDATE = pathlib.Path(__file__).parent / "BDNS to IFC.csv"

df_bdns = pd.read_csv(BDNS_REGISTER)
df_alex = pd.read_csv(BDNS_ALEX_UPDATE)

# to match the formatting of the updated BDNS file wrt to Types and NOTDEFINED etc. I'll apply the same
# changes I've made to the main BDNS file to the Alex update file

df_alex["ifc2x3_update"] = df_alex["IFC2x3"]
df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].str.replace(".", "")
df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].str.replace("NOTDEFINED", "")
df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].str.replace("USERDEFINED", "")
df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].str.strip()
df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].str.replace("Type", "")
df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].str.replace("Enum", "")
df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].str.replace("ifc", "Ifc")
df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].str.replace("Ifcvalve", "IfcValve")

df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].str.replace(
    "IfcElectricDistributionBoard", "IfcDistributionBoard"
)
df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].str.replace(".", "")
df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].str.replace(
    "NOTEDEFINED", ""
)  # fix typo
df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].str.replace(
    "NOT DEFINED", ""
)  # fix typo
df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].str.replace(
    "IfcSwitchingDevicePRESSURESENSOR", "IfcSwitchingDevice"
)  # fix error
df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].str.replace(
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


df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].fillna("")
df_alex["ifc2x3_update"] = df_alex["ifc2x3_update"].apply(remove_duplicates)

di_bdns = {
    f"{row.asset_abbreviation} | {row.asset_description}": row.ifc4_3
    for _, row in df_bdns.iterrows()
}
di_alex = {
    f"{row.asset_abbreviation} | {row.asset_description}": row.ifc2x3_update
    for _, row in df_alex.iterrows()
}

di_mult = {k: v for k, v in di_alex.items() if "," in v}

{print(f"{k} =  {v}") for k, v in di_mult.items()}
# > 
# ACT | actuator =  IfcActuatorPNEUMATICACTUATOR,IfcActuatorHANDOPERATEDACTUATOR,IfcActuatorTHERMOSTATICACTUATOR,IfcActuatorHYDRAULICACTUATOR,IfcActuator
# AT | air terminal - generic =  IfcAirTerminalIRIS,IfcAirTerminalLINEARGRILLE,IfcAirTerminalDIFFUSER,IfcAirTerminalLINEARDIFFUSER,IfcAirTerminalREGISTER,IfcAirTerminalGRILLE,IfcAirTerminal,IfcAirTerminalEYEBALL
# COIL | coil =  IfcCoilHYDRONICCOIL,IfcCoil
# CTFS | filter - cooling tower filtration unit =  IfcFilter,IfcUnitaryEquipment
# --- ^ these are multiple classes and need to be reviewed ^ ---

# I'll make a judgement call for now to go with the base / generic class definition: 
di_alex["ACT | actuator"] = "IfcActuator"
di_alex["AT | air terminal - generic"] = "IfcAirTerminal"
di_alex["COIL | coil"] = "IfcCoil"
di_alex["CTFS | filter - cooling tower filtration unit"] = "IfcFilter"

di_ifc2x3 = {k.split(" | ")[0]: v for k, v in di_alex.items()}
df_bdns["ifc2x3"] = df_bdns.asset_abbreviation.map(di_ifc2x3).fillna("")

df_bdns.to_csv(BDNS_REGISTER, index=False)
print("Updated BDNS Register with IFC2x3 classes")