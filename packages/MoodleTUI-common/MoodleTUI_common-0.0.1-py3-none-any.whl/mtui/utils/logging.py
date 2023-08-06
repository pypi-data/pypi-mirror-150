from rich.logging import RichHandler
from rich.console import Console
from logging import Logger
from enum import Enum


class LogLevel(Enum):
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40


def strToLogLevel(level: str) -> LogLevel:
    match level.upper():
        case "NOTSET":
            return LogLevel.NOTSET
        case "DEBUG":
            return LogLevel.DEBUG
        case "INFO":
            return LogLevel.INFO
        case "WARN":
            return LogLevel.WARN
        case "ERROR":
            return LogLevel.ERROR
        case _:
            return LogLevel.NOTSET


def buildLogger(level: str, console: Console) -> Logger:
    res = Logger("logger")
    handler = RichHandler(
        strToLogLevel(level).value,
        console=console,
        show_level=True,
        show_time=True,
        tracebacks_suppress=(KeyboardInterrupt, EOFError),
    )

    res.addHandler(handler)
    return res
