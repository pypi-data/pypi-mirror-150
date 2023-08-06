class Namespace:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, Namespace(**v) if isinstance(v, dict) else v)

    def __repr__(self):
        return "Namespace(%s)" % ", ".join(
            "=".join([k, repr(v)]) for k, v in self.__dict__.items()
        )
