from cryptography.fernet import Fernet, MultiFernet
from base64 import b85encode, b85decode
from pathlib import Path

from .types import Namespace
from .utils import buildDir


def genToken():
    token = Fernet.generate_key()
    yield Fernet(token), token.decode()


def getMultiFernet(config: Namespace = None, fernets: int = 5):
    metadata = config.Meta
    fernetPath = buildDir(
        "auth/keys.txt", metadata.app, metadata.author, metadata.version
    )

    # Generates a set of Fernet keys if it doesn't exist, else just read the file specified
    return (
        genMultiFernetFromFile(fernetPath)
        if fernetPath.exists()
        else genMultiFernet(config, fernets)
    )


def genMultiFernet(config: Namespace, fernets: int = 5):
    res = []

    for _ in range(fernets):
        (obj, token) = next(genToken())
        res.append(obj)
        dumpToken(token, config.Meta)

    return MultiFernet(res)


def genMultiFernetFromFile(file: Path):
    rawFernets = file.read_text().splitlines(False)
    return MultiFernet(map(lambda raw: Fernet(raw), rawFernets))


def dumpToken(token: str, metadata: Namespace):
    with open(
        # Would be somewhere in /home/<user>/.local/share/MoodleTUI/<version>/auth/keys.txt
        # on Linux, %AppData%/MoodleTUI/<version>/auth/keys.txt on Windows
        buildDir("auth/keys.txt", metadata.app, metadata.author, metadata.version),
        "a+",
    ) as f:
        content = f.readlines()
        content.append(token + "\n")

        f.writelines(content)


def encodeUserPassword(passwd: str | bytes | bytearray) -> str:
    passwd = passwd if isinstance(passwd, bytes | bytearray) else passwd.encode()
    return b85encode(passwd).decode()


def decodeUserPassword(passwd: str) -> str:
    return b85decode(passwd.encode()).decode()
