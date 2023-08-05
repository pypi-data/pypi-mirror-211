"""Return a valid config object from a toml file for the application."""

import tomli
from termcolor import cprint
import colorama

from .config import Config
from .constants import ERROR_COLOUR, LOCATION_ERR_MSG, INVALID_TOML_MSG

colorama.init()


class TomlConfig(Config):
    """
        A class to handle config files in toml format
    """

    def __init__(self, path: str, attrs: dict[str, list[type]] = {}):
        super().__init__(path, attrs)

    def _read_config(self) -> dict[str, object]:
        # Open the config file and return the contents as a dict
        try:
            with open(self.path, 'rb') as f_config:
                try:
                    return tomli.load(f_config)
                except tomli.TOMLDecodeError:
                    cprint(f"{INVALID_TOML_MSG} {self.path }", ERROR_COLOUR)
        except FileNotFoundError:
            cprint(f"{LOCATION_ERR_MSG} {self.path}", ERROR_COLOUR)
        return {}
