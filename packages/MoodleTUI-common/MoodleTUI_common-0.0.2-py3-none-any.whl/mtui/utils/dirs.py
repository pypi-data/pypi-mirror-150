from platformdirs import user_data_path


def buildDir(dir: str, app: str, author: str, version: str):
    base = user_data_path(app, author, version)
    res = base / dir

    for folder in res.parents[::-1]:
        if not folder.exists():
            folder.mkdir()

    return res
