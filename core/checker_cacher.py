from typing import Literal


class _CheckerCacher:
    def __init__(self):
        self._map: {str, (bool, str)} = {}

    @staticmethod
    def make_key(digest1: str, digest2: str, proj: int, unit: int, point: int):
        # if digest1 > digest2:
        #     digest1, digest2 = digest2, digest1
        return f"@{proj}.{unit}.{point}#{digest1}|{digest2}"

    def __call__(self, mode: Literal["load", "store"]):
        def aux_load(digest1: str, digest2: str, proj: int, unit: int, point: int):
            key = _CheckerCacher.make_key(digest1, digest2, proj, unit, point)
            if key not in self._map:
                return None, None
            else:
                return self._map[key]

        def aux_store(res: (bool, str), digest1: str, digest2: str, proj: int, unit: int, point: int):
            key = _CheckerCacher.make_key(digest1, digest2, proj, unit, point)
            self._map[key] = res
            print(f"Update Cache for {key}")

        return aux_load if mode == "load" else aux_store


_instance = _CheckerCacher()
LoadCheckerData = _instance("load")
StoreCheckerData = _instance("store")
