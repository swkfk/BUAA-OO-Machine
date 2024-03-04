from typing import Callable

import timeout_decorator

from core.checker_cacher import LoadCheckerData, StoreCheckerData
from core.default_checker import Fn as default_checker
from core.fs import COURSE_ROOT, JsonLoader, DB_ROOT, GetPointTimestamp, POINT_ROOT
from checkers import Checkers


async def GetDiffSame(proj: int, unit: int, point: int, user: str):
    submit_file = COURSE_ROOT / f"{proj}" / f"{unit}.submit.json"
    if not submit_file.exists():
        return [], []
    submit_obj: {str, str} = await JsonLoader(submit_file)
    if user not in submit_obj:
        return [], []

    course_obj = await JsonLoader(DB_ROOT / "course.json")
    unit_obj = course_obj[proj]["units"][unit]
    checker_s: str = unit_obj["judge"]

    if checker_s == "":
        raw_checker: Callable = default_checker
        compare_all = True
    else:
        raw_checker: Callable = Checkers[checker_s][1]
        compare_all = Checkers[checker_s][0]

    def checker(**kwargs):
        try:
            return timeout_decorator.timeout(1)(raw_checker)(**kwargs)
        except timeout_decorator.TimeoutError:
            return False, "Checker Timeout!"

    timestamp = await GetPointTimestamp(proj, unit, point)
    stdout_path = POINT_ROOT / f"{timestamp}" / "stdout"
    ret_v_path = POINT_ROOT / f"{timestamp}" / "return_value"

    if not (ret_v_path / user).exists():
        return [], []
    if "0" != (ret_v_path / user).read_text():
        return [], []

    self_digest = submit_obj[user]

    same, diff = [], []
    if compare_all:
        for other_user, other_digest in submit_obj.items():
            if other_user == user or other_user.startswith("__TEMP__"):
                continue
            res, msg = LoadCheckerData(self_digest, other_digest, proj, unit, point)
            if res is None:
                res, msg = checker(
                    fin=(POINT_ROOT / f"{timestamp}" / "stdin").open("r"),
                    fout=(stdout_path / user).open("r"),
                    fcmp=(stdout_path / other_user).open("r")
                )
                StoreCheckerData((res, msg), self_digest, other_digest, proj, unit, point)
            (same if res else diff).append(other_user)
    else:
        res, msg = LoadCheckerData(self_digest, self_digest, proj, unit, point)
        if res is None:
            res, msg = checker(
                fin=(POINT_ROOT / f"{timestamp}" / "stdin").open("r"),
                fout=(stdout_path / user).open("r")
            )
            StoreCheckerData((res, msg), self_digest, self_digest, proj, unit, point)
        (same if res else diff).append("[checker] " + msg)

    return same, diff
