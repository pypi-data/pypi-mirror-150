
def singleton(cls):

    setattr(cls, f"_{cls.__name__}__instance", None)

    return cls


def check_singleton(fn):
    def wrapper(self, *args):
        if not getattr(self, f"_{self.__class__.__name__}__instance", None):
            raise Exception("Singleton has not yet been initialized")
        
        return fn(self, *args)

    return wrapper