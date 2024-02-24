from typing import IO


def _check_main(**kwargs) -> (bool, str):
    """
    Thing will be provided:
    "fin" IO, stdin file
    "fout" IO, stdout file
    "fcmp" IO, other's stdout file (if CompareType == True)
    :return: bool - Whether correct or not
             str  - The information
    """
    _ = kwargs.get("fin")
    fout: IO = kwargs.get("fout")
    fcmp: IO = kwargs.get("fcmp")
    out = fout.read().strip().split('\n')
    other = fcmp.read().strip().split('\n')
    if len(out) != len(other):
        return False, "Different lines"
    for i in range(len(out)):
        if out[i].strip() != other[i].strip():
            return False, f"Conflict at line {i + 1}"
    return True, "Same"


# Information Needed for the checker_core
CompareType = True  # Is the checker needed to compare your stdout with others'
Fn = _check_main
