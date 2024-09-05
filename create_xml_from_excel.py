from lxml import etree
import pandas as pd
import json
import os
import re
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
from validator import validate_xml


def unflatten_json(flat_json):
    unflattened =  {}
    for key, value in flat_json.items():
        if key == "CREATED": continue
        parts = key.split(".")
        data = unflattened
        for part in parts[:-1]:
            if part not in data:
                data[part]=data.setdefault(part, {})
            data = data[part]
        data[parts[-1]] = value
    return unflattened

def create_xml_from_series_dict(json_data, name, xsd_location):

    # Function to convert dictionary to XML with custom rules
    def custom_dict_to_xml(data, root_name, namespace):
        def convert_dict_to_xml_recurse(parent, dict_item):
            for key, value in dict_item.items():
                if isinstance(value, dict) and len(value) == 1:
                    # Convert single child element to attribute
                    for sub_key, sub_value in value.items():
                        child = doc.createElement(key)
                        child.setAttribute(sub_key, str(sub_value))
                        parent.appendChild(child)
                elif isinstance(value, dict):
                    child = doc.createElement(key)
                    convert_dict_to_xml_recurse(child, value)
                    parent.appendChild(child)
                else:
                    child = doc.createElement(key)
                    child.appendChild(doc.createTextNode(str(value)))
                    parent.appendChild(child)
    
        doc = parseString('<{}></{}>'.format(root_name, root_name))
        root = doc.documentElement
        root.setAttribute("xmlns", namespace)
       
        convert_dict_to_xml_recurse(root, data)
        return doc.toprettyxml()
    
    # Convert JSON to dictionary
    data_dict = json.loads(json.dumps(json_data))
    
    # Convert dictionary to XML with custom rules
    xml_data = custom_dict_to_xml(data_dict, 'person', "http://www.example.com/person")

    # Sample function - convert text string with seperator to sequence elements
    def process_children(xml_string, sep=","):
        # Parse the XML string
        root = etree.fromstring(xml_string)
        namespace = {'ns': 'http://www.example.com/person'}

        # Navigate to the Children node
        children = root.find('.//ns:household/ns:children', namespaces=namespace)

        # Split the text content into individual child names
        names = children.text.split(sep)

        # Clear the original text content
        children.clear()

        # Add new child elements
        for name in names:
            new_element = etree.SubElement(children, 'child')
            new_element.set('name', name.strip())

        # Add xmlns:xsi and xsi:schemaLocation attributes to the root element
        root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", "http://www.example.com/person ../person.xsd")

        # Convert the modified XML back to a string
        modified_xml = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode('UTF-8')
        return modified_xml

    # Sample function - converting child nodes to element attributes
    def process_partner_element(xml_string):
        # Parse the XML string
        root = etree.fromstring(xml_string.encode("utf-8"))
        namespace = {'ns': 'http://www.example.com/person'}

        # Navigate to the partner node
        partner = root.find('.//ns:household/ns:partner', namespaces=namespace)

        if partner is not None:
            # Extract age and name elements
            age_element = partner.find('.//ns:age', namespaces=namespace)
            name_element = partner.find('.//ns:name', namespaces=namespace)
            
            if age_element is not None and name_element is not None:
                age = age_element.text
                name = name_element.text
                
                # Clear the partner element
                partner.clear()
                
                # Set the attributes
                partner.set('age', age)
                partner.set('name', name)
            else:
                print("Error: 'age' or 'name' element not found in 'partner'.")
        else:
            print("Error: 'partner' element not found.")
            
        # Convert the modified XML back to a string
        modified_xml = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode('UTF-8')
        return modified_xml


    xml_data = process_children(xml_data)
    xml_data = process_partner_element(xml_data)
    
    if not os.path.exists("converted"):
        os.makedirs("converted")
    
    # Save XML data to a file
    with open(f"converted/{name}.xml", "w") as f:
        f.write(xml_data)
    
    print(f"XML file for plant: {name} created!")
    
    validate_xml(f"converted/{name}.xml")

#endregion

df = pd.read_excel("docs/Persons.xlsx", index_col=3)
df_modified = df.drop(columns=['Unnamed: 0', 'Unnamed: 1', 'Attributes'])

for col in df_modified.columns:
    if not df_modified[col]["CREATED"] == True:
        flat_dict = df_modified[col].dropna()
        json_data = unflatten_json(flat_dict)
        create_xml_from_series_dict(json_data, flat_dict["personalInfo.name"], "../person.xsd")