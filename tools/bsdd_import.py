import pathlib
import csv
import json

BDNS_REGISTER = pathlib.Path(__file__).parent.parent / "BDNS_Abbreviations_Register.csv"
BSDD_IMPORT_BDNS = pathlib.Path(__file__).parent / "bsdd-import-bdns.json"

def read_csv(path: pathlib.Path) -> list[list]:
    """Read a CSV file and return its content as a list of lists."""
    data = list(csv.reader(path.read_text().split("\n")))
    if data[-1] == []:
        data = data[:-1]
    return data


# from: https://github.com/buildingSMART/bSDD/blob/master/Model/Import%20Model/bsdd-import-model.json
bsdd_import_template = {
    "ModelVersion": "2.0", # TODO: get from release
    "OrganizationCode": "bdns",
    "DictionaryCode": "bdns",
    "DictionaryName": "Building Device Naming Syntax",
    "DictionaryVersion": "2.1.0",
    "LanguageIsoCode": "EN",
    # "LanguageOnly": False,
    # "UseOwnUri": False,
    # "DictionaryUri": None,
    # "License": None,
    # "LicenseUrl": None, TODO
    # "ChangeRequestEmailAddress": None,
    # "MoreInfoUrl": None,
    # "QualityAssuranceProcedure": None,
    # "QualityAssuranceProcedureUrl": None,
    # "ReleaseDate": None,
    "Status": "Preview",
    # "Classes": [
    #   {
    #     "Code": None,
    #     "Name": None,
    #     "ClassType": None,
    #     "Definition": None,
    #     "Description": None,
    #     "ParentClassCode": None,
    #     "RelatedIfcEntityNamesList": [],
    #     "Synonyms": [],
    #     "ActivationDateUtc": None,
    #     "ReferenceCode": None,
    #     "CountriesOfUse": [],
    #     "CountryOfOrigin": None,
    #     "CreatorLanguageIsoCode": None,
    #     "DeActivationDateUtc": None,
    #     "DeprecationExplanation": None,
    #     "DocumentReference": None,
    #     "OwnedUri": None,
    #     "ReplacedObjectCodes": [],
    #     "ReplacingObjectCodes": [],
    #     "RevisionDateUtc": None,
    #     "RevisionNumber": None,
    #     "Status": None,
    #     "SubdivisionsOfUse": [],
    #     "Uid": None,
    #     "VersionDateUtc": None,
    #     "VersionNumber": None,
    #     "VisualRepresentationUri": None,
    #     "ClassProperties": [
    #       {
    #         "Code": None,
    #         "PropertyCode": None,
    #         "PropertyUri": None,
    #         "Description": None,
    #         "PropertySet": None,
    #         "Unit": None,
    #         "PredefinedValue": None,
    #         "IsRequired": None,
    #         "IsWritable": None,
    #         "MaxExclusive": None,
    #         "MaxInclusive": None,
    #         "MinExclusive": None,
    #         "MinInclusive": None,
    #         "Pattern": None,
    #         "OwnedUri": None,
    #         "PropertyType": None,
    #         "SortNumber": None,
    #         "Symbol": None,
    #         "AllowedValues": [
    #           {
    #             "Code": None,
    #             "Value": None,
    #             "Description": None,
    #             "Uri": None,
    #             "SortNumber": None,
    #             "OwnedUri": None
    #           }
    #         ]
    #       }
    #     ],
    #     "ClassRelations": [
    #       {
    #         "RelationType": None,
    #         "RelatedClassUri": None,
    #         "RelatedClassName": None,
    #         "Fraction": None,
    #         "OwnedUri": None
    #       }
    #     ]
    #   }
    # ],
    # "Properties": [
    #   {
    #     "Code": None,
    #     "Name": None,
    #     "Definition": None,
    #     "Description": None,
    #     "DataType": None,
    #     "Units": [],
    #     "Example": None,
    #     "ActivationDateUtc": None,
    #     "ConnectedPropertyCodes": [],
    #     "CountriesOfUse": [],
    #     "CountryOfOrigin": None,
    #     "CreatorLanguageIsoCode": None,
    #     "DeActivationDateUtc": None,
    #     "DeprecationExplanation": None,
    #     "Dimension": None,
    #     "DimensionLength": None,
    #     "DimensionMass": None,
    #     "DimensionTime": None,
    #     "DimensionElectricCurrent": None,
    #     "DimensionThermodynamicTemperature": None,
    #     "DimensionAmountOfSubstance": None,
    #     "DimensionLuminousIntensity": None,
    #     "DocumentReference": None,
    #     "DynamicParameterPropertyCodes": [],
    #     "IsDynamic": False,
    #     "MaxExclusive": None,
    #     "MaxInclusive": None,
    #     "MinExclusive": None,
    #     "MinInclusive": None,
    #     "MethodOfMeasurement": None,
    #     "OwnedUri": None,
    #     "Pattern": None,
    #     "PhysicalQuantity": None,
    #     "PropertyValueKind": None,
    #     "ReplacedObjectCodes": [],
    #     "ReplacingObjectCodes": [],
    #     "RevisionDateUtc": None,
    #     "RevisionNumber": None,
    #     "Status": None,
    #     "SubdivisionsOfUse": [],
    #     "TextFormat": None,
    #     "Uid": None,
    #     "VersionDateUtc": None,
    #     "VersionNumber": None,
    #     "VisualRepresentationUri": None,
    #     "PropertyRelations": [
    #       {
    #         "RelatedPropertyName": None,
    #         "RelatedPropertyUri": None,
    #         "RelationType": None,
    #         "OwnedUri": None
    #       }
    #     ],
    #     "AllowedValues": [
    #       {
    #         "Code": None,
    #         "Value": None,
    #         "Description": None,
    #         "Uri": None,
    #         "SortNumber": None,
    #         "OwnedUri": None
    #       }
    #     ]
    #   }
    # ]
  }


bdns = read_csv(BDNS_REGISTER)
bdns = [dict(zip(bdns[0], row)) for row in bdns[1:]]

classes = [{"Code": x["asset_abbreviation"], "Name": x["asset_description"], "ClassType": "Class"} for x in bdns]

bsdd_import_template["Classes"] = classes
# BSDD_IMPORT_BDNS.write_text(json.dumps(bsdd_import_template, indent=4)) 
BSDD_IMPORT_BDNS.write_bytes(json.dumps(bsdd_import_template, indent=4).encode("utf-8"))

print("done")