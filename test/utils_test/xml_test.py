from yakshop.utils.xml_reader import read_xml
from yakshop.utils.config import get_root_path
import os


def test_read_xml():
    xml = read_xml(os.path.join(get_root_path(), "fake_db/herd.xml"))
    assert type(xml) == list
    assert len(xml) > 0
