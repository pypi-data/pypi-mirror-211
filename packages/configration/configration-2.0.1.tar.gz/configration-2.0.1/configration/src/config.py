"""Base class for config object for the application."""

from termcolor import cprint
import colorama

from .constants import ERROR_COLOUR, CORRUPT_FILE_MSG, MISSING_ATTR_MSG, NOT_OF_TYPE_MSG

colorama.init()


class Config():
    """
    The class takes a path to a json file and if valid, returns a config dict.

    Attributes
    ----------

    path: str
        The path to the config file

    attrs: dict[str, list[type]
        The dict keys are the fields that are expected in the config json
        The dict item holds a list of allowed types for each files

        If there are attrs, then the config is validated.
    """

    def __init__(self, path: str, attrs: dict[str, list[type]] = {}):
        self.path = path
        self.attrs = attrs
        self.config = self._get_config()
        for key, item in self.config.items():
            self.__dict__[key] = item

    def _get_config(self) -> dict[str, object]:
        # Return config, if contents are valid.
        config = self._read_config()

        if not self.attrs:
            return config

        if self._validate_config(config):
            return config
        return {}

    def _validate_config(self, config: dict[str, type]) -> bool:
        # Return True if structure and values in config are valid.
        for name, item_types in self.attrs.items():
            if name not in config:
                cprint(f"{CORRUPT_FILE_MSG} {MISSING_ATTR_MSG} {name}", ERROR_COLOUR)
                return False
            if type(config[name]) not in item_types:
                cprint(f"{CORRUPT_FILE_MSG} {name} {NOT_OF_TYPE_MSG} {item_types}", ERROR_COLOUR)
                return False
        return True
