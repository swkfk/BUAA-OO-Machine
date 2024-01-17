
def GetProjList():
    return ["P1: Hello World", "P2: A + B 问题"]


def GetUnitList(proj_id: int):
    if proj_id == 0:
        return ["U1: print"]
    else:
        return ["U1: Inout", "U2: Add"]


def GetPointInfo(proj_id: int, unit_id: int):
    if (proj_id, unit_id) == (0, 0):
        return [
            {"same": ["person0", "person2"], "diff": ["person1"]},
            {"same": ["person0", "person1", "person2"], "diff": []},
            {"same": [], "diff": ["person0", "person1", "person2"]},
            {"same": ["person0", "person1"], "diff": ["person2"]},
            {"same": ["person0"], "diff": ["person1", "person2"]},
            {"same": [], "diff": ["person0", "person1", "person2"]},
            {"same": ["person0", "person1"], "diff": ["person2"]},
            {"same": ["person0"], "diff": ["person1", "person2"]},
            {"same": [], "diff": ["person0", "person1", "person2"]},
            {"same": ["person0", "person1"], "diff": ["person2"]},
            {"same": ["person0"], "diff": ["person1", "person2"]},
        ]
    else:
        return [
            {"same": [], "diff": ["person0", "person1", "person2"]},
            {"same": ["person0", "person1"], "diff": ["person2"]},
            {"same": ["person0"], "diff": ["person1", "person2"]},
        ]
