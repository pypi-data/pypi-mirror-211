
from pathlib import Path

from ..src.toml_config import TomlConfig

CONFIG_ATTRS = {
    'period_start_month': [int],
    'payment_bbo': [int, float],
    'period_months': [int],
}


def test_config_structure():
    path = Path('tests', 'test_data', 'config.toml')
    config = TomlConfig(path)
    assert isinstance(config.config, dict)
    assert len(config.config) == 3


def test_config_missing(capsys):
    path = Path('tests', 'test_data', 'not_a_file.toml')
    err_msg = f'The config file is not in the expected location: {path}'
    TomlConfig(path)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'\x1b[31m{err_msg}\x1b[0m'


def test_config_invalid_attrs(capsys):
    path = Path('tests', 'test_data', 'config_invalid_attrs.toml')
    err_msg = "Corrupt config file. period_start_month not of type [<class 'int'>]"
    TomlConfig(path, CONFIG_ATTRS)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'\x1b[31m{err_msg}\x1b[0m'


def test_config_invalid_json(capsys):
    path = Path('tests', 'test_data', 'config_invalid_toml.toml')
    err_msg = f"Invalid toml format in {path}"
    TomlConfig(path)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'\x1b[31m{err_msg}\x1b[0m'


def test_config_missing_attr(capsys):
    path = Path('tests', 'test_data', 'config_missing_attr.toml')
    err_msg = f"Corrupt config file. Missing attribute: payment_bbo"
    TomlConfig(path, CONFIG_ATTRS)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'\x1b[31m{err_msg}\x1b[0m'
