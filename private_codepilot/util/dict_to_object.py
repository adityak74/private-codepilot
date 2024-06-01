"""Dict to Object Init"""


class Dict2Object:
    def __init__(self, d=None):
        if d is not None and isinstance(d, dict):
            for key, value in d.items():
                setattr(self, key, value)


if __name__ == "__main__":
    o = Dict2Object({"a": 1})
    print(o.a)
