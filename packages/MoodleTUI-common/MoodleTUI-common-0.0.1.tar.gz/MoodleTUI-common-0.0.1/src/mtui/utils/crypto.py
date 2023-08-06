from cryptography.fernet import MultiFernet


def encodePassword(key: MultiFernet, password: str) -> str:
    return key.encrypt(password.encode()).decode()


def decodePassword(key: MultiFernet, password: str) -> str:
    return key.decrypt(password.encode()).decode()
