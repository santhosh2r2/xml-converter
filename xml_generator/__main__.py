import pandas as pd
from create_xml_from_excel import create_xml_from_series_dict, unflatten_json
from validator import validate_xml

NAMESPACE = "http://www.example.com/person"
SCHEMA_LOCATION = "source/person.xsd"

if __name__ == "__main__":
    df = pd.read_excel("docs/Persons.xlsx", index_col=3)
    df_modified = df.drop(columns=['Unnamed: 0', 'Unnamed: 1', 'Attributes'])

    for col in df_modified.columns:
        if not df_modified[col]["CREATED"] == True:
            flat_dict = df_modified[col].dropna()
            json_data = unflatten_json(flat_dict)
            name= flat_dict["personalInfo.name"]
            create_xml_from_series_dict(json_data,name, NAMESPACE, SCHEMA_LOCATION)
            validate_xml(f"converted/{name}.xml", SCHEMA_LOCATION)