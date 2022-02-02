from yakshop.utils.xml_reader import read_xml
from typing import List


class FakeDBHandler(object):
    def __init__(self, data: List[dict] = None):
        self.data = data

    @classmethod
    def init_database_connection_fake(cls, path: str):
        return cls(read_xml(path_to_file=path))

    def get_all_yaks(self) -> List[dict]:
        return self.data

    def get_yak(self, name: str) -> dict:
        try:
            for yak_dict in self.data:
                if yak_dict["name"] == name:
                    return yak_dict

        except KeyError:
            # log here
            raise KeyError
