class SessionState:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get(cls, **kwargs):
        session = cls(**kwargs)
        return session

    def set(self, key, value):
        setattr(self, key, value)
