from ..src.json_config import JsonConfig


def test_config_instantiate():
    config = JsonConfig()
    assert config


def test_always_passes():
    assert True


def test_always_fails():
    assert False