from configparser import ConfigParser, NoSectionError


class UserConfigs:
    """Class that represents UserConfigs (token, verbose, etc)"""

    _settings: dict = {
        "verbose": False,
    }
    _filename: str = "configs.json"

    def set_verbose(self, verbose: bool):
        """
        Setter for verbose key in the dictionary
        :param verbose: bool parameter
        :return:
        """
        self._settings["verbose"] = verbose

    def set_token(self, token: str):
        """
        Setter for a token string.
        :param token:  token
        :return:
        """
        self._settings["token"] = token

    def get_verbose(self) -> bool:
        """
        Getter for a verbose parameter
        :return: verbose value if exists, False instead
        """
        if "verbose" not in self._settings:
            return False
        return self._settings["verbose"]

    def get_auth_token(self) -> str:
        """
        Get token that will be used for user authentication
        :return: token
        """
        if "token" not in self._settings:
            raise ValueError("Authorization token is not present")
        return self._settings["token"]

    def _read_from_dict(self, **kwargs):
        """Create configs form the dictionary"""
        if "token" not in kwargs:
            raise ValueError("Authorization token is not present")

        self._settings = {**self._settings, **kwargs}

    def _read_from_ini_file(self):
        """Create configs from the ini file"""
        config = ConfigParser()
        config.read(self._filename)

        if "user_configs" not in config:
            return

        if "authorization" not in config:
            raise NoSectionError("Authorization section is not present")

        new_settings = {}
        # user_configs
        self._add_option(config, "user_configs", "verbose", bool, new_settings)

        # authorization
        self._add_option(config, "authorization", "token", str, new_settings)

        self._settings.update(new_settings)

    def __init__(self, user_settings: dict = None):
        """
        Constructor to init global parameters for a user_config (read from configs.json) file.
        """
        if user_settings:
            self._read_from_dict(**user_settings)
        else:
            self._read_from_ini_file()

    def __str__(self):
        return str(self._settings)

    @staticmethod
    def _add_option(config: ConfigParser, section: str, option: str, data_type: type, result: dict):
        if not config.has_option(section, option):
            return

        try:
            if data_type is int:
                result[option] = config.getint(section, option)
            elif data_type is float:
                result[option] = config.getfloat(section, option)
            elif data_type is bool:
                result[option] = config.getboolean(section, option)
            else:
                result[option] = config.get(section, option)
        except ValueError:
            # Ignore wrong value param and write the message
            print(f"INFO: Wrong value for the parameter {option} it should be {data_type}")
