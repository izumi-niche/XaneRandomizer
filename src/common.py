import xml.etree.ElementTree as ET
import os
import sys
import io

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def LoadXml(location):
	parser = ET.XMLParser(encoding="utf-8")
	tree = ET.parse(resource_path(location), parser=parser)
	return tree.getroot()

def ByteToInt(number):
	return int.from_bytes(number, byteorder=sys.byteorder)