import logging
from lxml import etree
from logger import log_message, setup_logger

LOGGER = setup_logger("validate-xml", logging.DEBUG)


def validate_xml(filepath, schema_location):
    # Load the XML and XSD files
    xml_file = filepath
    xsd_file = schema_location

    with open(xml_file, 'rb') as xml:
        xml_content = xml.read()

    with open(xsd_file, 'rb') as xsd:
        xsd_content = xsd.read()

    # Parse the XML and XSD
    xml_doc = etree.XML(xml_content)
    xsd_doc = etree.XMLSchema(etree.XML(xsd_content))

    # Validate the XML against the XSD
    is_valid = xsd_doc.validate(xml_doc)

    if is_valid:
        log_message(LOGGER, logging.INFO,
                    f"The XML document {filepath} is valid.")
    else:
        log_message(LOGGER, logging.INFO,
                    f"The XML document {filepath} is invalid.")
        for error in xsd_doc.error_log:
            log_message(LOGGER, logging.ERROR, error.message)
