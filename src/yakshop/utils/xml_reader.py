import os.path
import xml.etree.ElementTree as ET
from yakshop.utils.config import get_root_path
from typing import List


def read_xml(path_to_file: str) -> List[dict]:
    xml_path = os.path.join(get_root_path(), path_to_file)
    return [labyak.attrib for labyak in ET.parse(source=xml_path).getroot()]
