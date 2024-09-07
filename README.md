# XML-Generator

This creates `xml` files from Excel file.

## Excel file prepration

- Columns 1 and 2 - Eontains the element. Further levels can be added, in column 2, by using "." as separator. 
- Column 3 - Attribute for the parent element
- Column 4 and above - the data for XML file is entered

```sh
# Install and activate the environment 
poetry install && poetry shell

# Execute the script
python xml_generator

```

