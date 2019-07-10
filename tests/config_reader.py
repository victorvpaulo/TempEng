from configparser import ConfigParser
from pathlib import Path

ROOT = current_path = Path(__file__).parent


def build_config_parser():
    config_file_path = Path(ROOT / "config/configurations.config").resolve()
    parser = ConfigParser()
    parser.read(config_file_path)
    return parser


def get_configuration_value(section, key):
    parser = build_config_parser()
    return parser.get(section, key)


def get_path_from_config(path_key):
    path = Path(str(ROOT) + get_configuration_value("PATHS", path_key))
    return path
