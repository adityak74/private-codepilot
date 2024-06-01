"""Get App Config"""

from dotenv import dotenv_values
from private_codepilot.util.dict_to_object import Dict2Object
from private_codepilot.core.constants import Constants


class Config:
    """Config"""

    def __init__(self):
        """Initialize Config"""
        self.app_config = Dict2Object(dotenv_values(Constants.ENV_FILE.value))
