"""Return a valid config object from a json file for the application."""

import json
from termcolor import cprint
import colorama

from .config import Config
from .constants import ERROR_COLOUR, LOCATION_ERR_MSG, INVALID_JSON_MSG

colorama.init()


class JsonConfig(Config):
    """
        A class to handle config files in json format
    """

    def __init__(self, path: str, attrs: dict[str, list[type]] = {}):
        super().__init__(path, attrs)

    def _read_config(self) -> dict[str, object]:
        # Open the config file and return the contents as a dict
        try:
            with open(self.path, 'r') as f_config:
                try:
                    return json.load(f_config)
                except json.decoder.JSONDecodeError:
                    cprint(f"{INVALID_JSON_MSG} {self.path }", ERROR_COLOUR)
        except FileNotFoundError:
            cprint(f"{LOCATION_ERR_MSG} {self.path}", ERROR_COLOUR)
        return {}
