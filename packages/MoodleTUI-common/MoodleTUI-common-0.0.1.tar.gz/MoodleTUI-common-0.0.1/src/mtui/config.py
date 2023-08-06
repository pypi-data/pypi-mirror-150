from configparser import ConfigParser
from pathlib import Path
from .types import Namespace


def load(file: Path):
    config = ConfigParser()

    config.read(file)

    return Namespace(
        **{
            section: Namespace(
                **{
                    header: toInt(config.get(section, header).strip('"'))
                    for header in config[section]
                }
            )
            for section in config.sections()
        }
    )


def toInt(num: str) -> int:
    try:
        return int(num)
    except ValueError:
        return num
