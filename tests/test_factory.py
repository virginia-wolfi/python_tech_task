from to_do_list import create_app
from to_do_list.config import TestingConfig


def test_config():
    assert not create_app().testing
    assert create_app(config_obj=TestingConfig()).testing
