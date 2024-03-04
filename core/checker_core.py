from typing import Callable

import timeout_decorator

from checkers.CheckerMetadata import CheckerMetadata
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
        compare_type = CheckerMetadata.Mutual
    else:
        raw_checker: Callable = Checkers[checker_s][1]
        compare_type = Checkers[checker_s][0]

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

    def compare_all(c_user, c_digest, o_user, o_digest):
        res, msg = LoadCheckerData(c_digest, o_digest, proj, unit, point)
        if res is None:
            res, msg = checker(
                fin=(POINT_ROOT / f"{timestamp}" / "stdin").open("r"),
                fout=(stdout_path / c_user).open("r"),
                fcmp=(stdout_path / o_user).open("r")
            )
            StoreCheckerData((res, msg), c_digest, o_digest, proj, unit, point)
        return res, msg

    def compare_self(c_user, c_digest):
        res, msg = LoadCheckerData(c_digest, c_digest, proj, unit, point)
        if res is None:
            res, msg = checker(
                fin=(POINT_ROOT / f"{timestamp}" / "stdin").open("r"),
                fout=(stdout_path / c_user).open("r")
            )
            StoreCheckerData((res, msg), c_digest, c_digest, proj, unit, point)
        return res, msg

    match compare_type:
        case CheckerMetadata.Mutual:
            for other_user, other_digest in submit_obj.items():
                if other_user == user or other_user.startswith("__TEMP__"):
                    continue
                r, m = compare_all(user, submit_obj[user], other_user, other_digest)
                (same if r else diff).append(f"({other_user}): " + m)
        case CheckerMetadata.Checker:
            r, m = compare_self(user, submit_obj[user])
            (same if r else diff).append("[Checker]: " + m)
        case CheckerMetadata.Both:
            r, m = compare_self(user, submit_obj[user])
            (same if r else diff).append("[Checker]: " + m)
            if not r:
                return same, diff
            for other_user, other_digest in submit_obj.items():
                if other_user == user or other_user.startswith("__TEMP__"):
                    continue
                if not compare_self(other_user, other_digest)[0]:
                    continue
                r, m = compare_all(user, submit_obj[user], other_user, other_digest)
                (same if r else diff).append(f"({other_user}): " + m)

    return same, diff
