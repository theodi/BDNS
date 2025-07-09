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

def ifc_strip_enum(ifc_class: str) -> str:
    return re.sub(r"([A-Z0-9_]+_?)$", "", ifc_class)


def ifc_class_is_enum(ifc_class: str) -> bool:
    return ifc_strip_enum(ifc_class) != ifc_class


def get_map_ifc_bdns(abbreviations): #, core_only=True
    # if core_only:
    #     ifc_classes = {k: v for k, v in ifc_classes.items() if not ifc_class_is_enum(k)}
    map_bdns_ifc = {x[1]: x[-3] for x in abbreviations[1:]}
    ifc_in_bdns = set([x[-3] for x in abbreviations[1:]])

    map_ifc_bdns = {}
    for ifc in ifc_in_bdns:
        map_ifc_bdns[ifc] = [k for k, v in map_bdns_ifc.items() if v == ifc]

    map_ifc_bdns = {k: v for k, v in map_ifc_bdns.items() if not ifc_class_is_enum(k)}
    return map_ifc_bdns


abbreviations = read_csv(BDNS_REGISTER)
map_ifc_bdns = get_map_ifc_bdns(abbreviations)
one_to_one = {k:v for k, v in map_ifc_bdns.items() if len(v) == 1}
one_to_many = {k:v for k, v in map_ifc_bdns.items() if len(v) > 1}
li_one_to_one = list(itertools.chain.from_iterable(one_to_one.values()))
li_one_to_many = list(itertools.chain.from_iterable(one_to_many.values()))


# where one_to_one define the mapping as the default
indexes = [n for n, x in enumerate(abbreviations) if x[1] in li_one_to_one]
for n in indexes:
    abbreviations[n][-1] = 1  # Set the last column to 1 (is_ifc_default) for one-to-one mappings

# where there is a one_to_many we must choose a default

# needs review:
# IfcFlowTerminal
# IfcElectricFlowStorageDevice
# IfcFlowTreatmentDevice

default_mappings = {
#   "IfcFlowTerminal": [
#     "CKCGR",
#     "CKGRCK",
#     "CKGWR"
#   ],
  "IfcInterceptor": [
    "INT",
    # "SSP"
  ],
  "IfcPump": [
    # "FJP",
    # "FP",
    "PMP",
    # "CNP",
    # "AXCWP",
    # "BSP",
    # "CHWP",
    # "CDWP",
    # "CTSEPP",
    # "DHWP",
    # "DP",
    # "FHP",
    # "FOP",
    # "GBP",
    # "GWBP",
    # "HXP",
    # "HTCHP",
    # "HTCWP",
    # "HWP",
    # "LTCHWP",
    # "LTCDWP",
    # "LTHWP",
    # "PAPS",
    # "DWBP",
    # "DWTP",
    # "PCHWP",
    # "PP",
    # "PCWP",
    # "PWP",
    # "RNWBP",
    # "RNWP",
    # "RCP",
    # "RWP",
    # "SCHWP",
    # "SHCP",
    # "SHWP",
    # "SP",
    # "SEPP",
    # "SEP",
    # "SPP",
    # "TMUP",
    # "TRP",
    # "VCP",
    # "WWP",
    # "WRP"
  ],
  "IfcMotorConnection": [
    "MCN",
    # "VSD",
    # "VFD"
  ],
  "IfcAirTerminal": [
    # "EAV",
    # "SAV",
    "AT",
    # "GR",
    # "EG",
    # "SG",
    # "LOU",
    # "ELOU",
    # "ILOU"
  ],
  "IfcTransformer": [
    # "DCDC",
    # "PVTXMR",
    "TXMR"
  ],
#   "IfcElectricFlowStorageDevice": [
#     "BATTLI",
#     "LB"
#   ],
  "IfcElectricAppliance": [
    # "BVAP",
    # "BVC",
    # "BVCFMG",
    # "BVCFM",
    # "BVCFMN",
    # "BVCFMU",
    # "BVCFME",
    # "BVS",
    # "FCSD",
    # "CKBP",
    # "CKDSTE",
    # "CKGRD",
    # "CKKET",
    # "CKPBP",
    # "CKPSTE",
    # "CKROT",
    # "CKSTE",
    # "DISP",
    # "DISPB",
    # "DISPC",
    # "DISPIB",
    # "DISPJ",
    # "DISPMK",
    # "DISPIC",
    # "DISPW",
    # "ELOCK",
    # "EMDH",
    # "LLOCK",
    # "MLOCK",
    "EAPPL",
    # "ADY",
    # "EPOS",
    # "GYMEQ",
    # "FOODEQ",
    # "HDY",
    # "STE",
    # "ETCFP",
    # "FSCPL",
    # "FSCWL",
    # "FSHCPL",
    # "FSHCWL",
    # "FSHPL",
    # "FSHWL",
    # "FSICD",
    # "FSIWL",
    # "FSIW",
    # "FSSWL",
    # "KSTCH",
    # "KSMBL",
    # "KBBL",
    # "KBC",
    # "KCO",
    # "KCWM",
    # "KCDY",
    # "KDR",
    # "KDPR",
    # "KICT",
    # "KJC",
    # "KMBS",
    # "KMM",
    # "KMS",
    # "KMIX",
    # "KPM",
    # "KPPM",
    # "KFS",
    # "KSBL",
    # "KTST",
    # "KUVSC",
    # "KVPM",
    # "KVCM",
    # "KVWM",
    # "KVW",
    # "IM",
    # "WSTFD",
    # "WSTC",
    # "WSTWG",
    # "IWH"
  ],
  "IfcBurner": [
    # "FR",
    "BUR"
  ],
  "IfcLightFixture": [
    "LT",
    # "DL",
    # "EL",
    # "UL",
    # "WL",
    # "LBO",
    # "LPO"
  ],
  "IfcDuctSegment": [
    "DUW",
    # "FDUW"
  ],
  "IfcDistributionBoard": [
    "DB",
    # "ITDP",
    # "KDP",
    # "MPNL",
    # "MDU",
    # "PB",
    # "PDU",
    # "RMU"
  ],
  "IfcGroup": [
    "GRP",
    # "LGRP"
  ],
#   "IfcFlowTreatmentDevice": [
#     "ADS",
#     "AS"
#   ],
  "IfcCompressor": [
    "CMP",
    # "ACP"
  ],
  "IfcCableCarrierSegment": [
    # "CABASK",
    "CCS"
  ],
  "IfcCommunicationsAppliance": [
    "CMA",
    # "DPU",
    # "HMI",
    # "IDF",
    # "SRV",
    # "NAM",
    # "NMS",
    # "PDUIPD",
    # "POEETS",
    # "SDNC",
    # "UPSMS",
    # "LBCN"
  ],
  "IfcElectricMotor": [
    "EMT",
    # "SDM",
    # "ELDM",
    # "ELTM"
  ],
  "IfcEvaporativeCooler": [
    # "HYAC",
    "EVCL"
  ],
  "IfcDamper": [
    "DMP",
    # "EXD",
    # "IISD",
    # "MD"
  ],
  "IfcUnitaryEquipment": [
    # "USS",
    # "FCU",
    # "CTFU",
    # "PFU",
    # "HIU",
    # "ASHP",
    # "GSHP",
    # "HP",
    # "WSHP",
    # "PU",
    # "WMS",
    "UEQ",
    # "CTSU"
  ],
  "IfcChiller": [
    "CH",
    # "CCCH",
    # "HTCH",
    # "LTCH"
  ],
  "IfcUnitaryControlElement": [
    # "LCM",
    # "LCP",
    # "CTCP",
    # "FACP",
    # "MCC",
    # "RIO",
    # "VAVCTR",
    # "ELC",
    "UCE"
  ],
  "IfcShadingDevice": [
    # "BL",
    "SHD"
  ],
  "IfcElectricFlowTreatmentDevice": [
    # "PFC",
    "EFT"
  ],
  "IfcFireSuppressionTerminal": [
    # "GSH",
    "FSP"
  ],
  "IfcWasteTerminal": [
    # "BVKOC",
    "WSTT",
    # "AD"
  ],
  "IfcCableSegment": [
    # "DCA",
    "CA",
    # "FCA",
    # "TR",
    # "EBA",
    # "ERO",
    # "ETA"
  ],
  "IfcAirTerminalBox": [
    "ATB",
    # "FPB",
    # "UFT",
    # "VAV",
    # "VAVE",
    # "VAVS",
    # "VVTB",
    # "VVT",
    # "KVVC"
  ],
  "IfcSwitchingDevice": [
    # "AIC",
    # "VIC",
    "SWD",
    # "STS",
    # "HTCO",
    # "IFU",
    # "FMO",
    # "FS",
    # "LSW",
    # "APSW",
    # "DEWSW",
    # "DPSW",
    # "SPSW",
    # "TDSW"
  ],
  "IfcAirToAirHeatRecovery": [
    # "MVHR",
    "HRU",
  ],
  "IfcFilter": [
    "FLT",
    # "APU",
    # "AWSH",
    # "BFLT",
    # "CFLT",
    # "CTFS",
    # "CTSFLT",
    # "CTSEP",
    # "CTSSEP",
    # "DGA",
    # "DTS",
    # "DSU",
    # "PFLT",
    # "RO",
    # "SSFLT",
    # "VSFLT",
    # "RRFLT",
    # "UVDU"
  ],
  "IfcWindow": [
    # "ECG",
    "WD"
  ],
  "IfcProtectiveDevice": [
    # "BTR",
    # "ATS",
    # "EISOTX",
    "PDV"
  ],
  "IfcOutlet": [
    "OUT",
    # "FLRB",
    # "LER"
  ],
  "IfcTank": [
    "TK",
    # "DEA",
    # "DET",
    # "EST",
    # "FODT",
    # "DWTT",
    # "CHDU",
    # "DPOT"
  ],
  "IfcFastener": [
    # "CIS",
    # "ECL",
    "FSTN"
  ],
  "IfcAlarm": [
    "ALR",
    # "PDB",
    # "FAS"
  ],
  "IfcFurniture": [
    "FUR",
    # "EKC",
    # "FSSG",
    # "CSC",
    # "KSTC",
    # "KCART",
    # "LCKR",
    # "WSTBIN"
  ],
  "IfcSpaceHeater": [
    # "FSHL",
    # "DH",
    # "EUH",
    # "GUH",
    "HTR",
    # "TC",
    # "EHT",
    # "TRHC",
    # "TRH",
    # "UFM",
    # "UH",
    # "WAC",
    # "CCH"
  ],
  "IfcValve": [
    # "TMUV",
    # "TP",
    # "TPE",
    "VLV",
    # "AV",
    # "BFP",
    # "BDV",
    # "BFV",
    # "CHWV",
    # "CDWV",
    # "CV",
    # "CVM",
    # "CVO",
    # "DPCV",
    # "ENV",
    # "FV",
    # "FCV",
    # "HWV",
    # "LCV",
    # "MUV",
    # "MMV",
    # "PA",
    # "PCV",
    # "PICV",
    # "PWV",
    # "RCV",
    # "RTV",
    # "SGV",
    # "SPRV",
    # "SPV",
    # "TCV",
    # "WHAV"
  ],
  "IfcFan": [
    "FAN",
    # "CTF",
    # "ELVPF",
    # "EF",
    # "GSF",
    # "GTF",
    # "KEF",
    # "MEV",
    # "MEVK",
    # "PF",
    # "RLF",
    # "RTF",
    # "SEF",
    # "SPF",
    # "SF",
    # "TEF",
    # "TF"
  ],
  "IfcAudioVisualAppliance": [
    "AVEQ",
    # "AAE",
    # "AMIX",
    # "MIX",
    # "AVKP",
    # "AVE",
    # "AVO",
    # "AVS",
    # "BTAI",
    # "CCU",
    # "CD",
    # "DEC",
    # "CMS",
    # "MSW",
    # "RBP",
    # "TCD",
    # "TPAN",
    # "VMIX",
    # "WNG",
    # "WPD",
    # "WRCVR",
    # "WSEND"
  ],
  "IfcSensor": [
    # "HDS",
    "SNS",
    # "GLYPR",
    # "IMUS",
    # "LDS",
    # "LVLS",
    # "LTMTS",
    # "MCS",
    # "MTS",
    # "NDS",
    # "PMS",
    # "PCS",
    # "SSS",
    # "VS",
    # "VBS"
  ],
  "IfcFlowMeter": [
    "MTR",
    # "EBM",
    # "EMV",
    # "FM",
    # "GMV",
    # "HM",
    # "HMV",
    # "WMV"
  ],
  "IfcController": [
    # "RFIDC",
    "CNTRL",
    # "IRRC",
    # "ROC",
    # "PVDAS",
    # "PVMC",
    # "PVMLPE",
    # "SDC"
  ],
  "IfcDistributionSystem": [
    "DSYS",
    # "KUDS",
    # "KUCS"
  ]
}

li_default_mappings = list(itertools.chain.from_iterable(default_mappings.values()))
li_one_to_many = [x for x in li_one_to_many if x not in li_default_mappings]

indexes = [n for n, x in enumerate(abbreviations) if x[1] in li_one_to_many]
for n in indexes:
    abbreviations[n][-3] = abbreviations[n][-3] + "NOTDEFINED"
    abbreviations[n][-2] = abbreviations[n][-2] + "NOTDEFINED"
    # ^ for the one-to-many mappings that are not the default make them "NOTDEFINED"


indexes = [n for n, x in enumerate(abbreviations) if x[1] in li_default_mappings]
for n in indexes:
    abbreviations[n][-1] = 1
    # ^ for the one-to-many set the default mappings


write_csv(BDNS_REGISTER, abbreviations)