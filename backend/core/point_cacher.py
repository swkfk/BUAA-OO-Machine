_point_cacher = {}

def _make_key(user: str, proj: int, unit: int) -> str:
    return f"{user}@{proj}@{unit}"

def PopPointData(user: str, proj: int, unit: int):
    key = _make_key(user, proj, unit)
    if key in _point_cacher:
        return _point_cacher.pop(_make_key(user, proj, unit))
    return []

def PushPointData(user: str, proj: int, unit: int, data: []):
    _point_cacher[_make_key(user, proj, unit)] = data
