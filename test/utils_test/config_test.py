from yakshop.utils.config import get_root_path, read_yaml


def test_read_yaml():
    yaml_right = read_yaml(root_path=get_root_path())
    assert type(yaml_right) == dict
    assert yaml_right
