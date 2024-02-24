import os.path
import sys
import json
from pathlib import Path


class ArgvCountError(Exception):
    def __init__(self, got: int, expect: int):
        super().__init__(self)
        self.got = got
        self.expect = expect

    def __str__(self):
        return f"ArgvCountError('Wrong arguments quantity, got `{self.got}`, expected `{self.expect}`')"


class ArgvWrongError(Exception):
    def __init__(self, got: str, expect: [str]):
        super().__init__(self)
        self.got = got
        self.expect = expect

    def __str__(self):
        return f"ArgvWrongError('Wrong argument, got `{self.got}`, expected `{self.expect}`')"


class InputError(Exception):
    def __init__(self, got, reason: str):
        super().__init__(self)
        self.got = got
        self.reason = reason

    def __str__(self):
        return f"InputError('Bad input: `{self.got}`, for `{self.reason}`')"


def _add_op(argv: [str]):
    if len(argv) != 2:
        raise ArgvCountError(len(argv), 2)

    expect_item = ["proj", "unit"]
    if argv[1] not in expect_item:
        raise ArgvWrongError(argv[1], expect_item)

    course_file = "database/course.json"
    if not os.path.exists(course_file):
        with open(course_file, "w") as f:
            f.write("[]")

    f = open(course_file, "r")
    # Load the current courses and display them
    obj = json.load(f)
    print("======== Course List ========")
    for proj_id, proj in enumerate(obj):
        print(f"#{proj_id}: {proj['title']}")
        for unit_id, unit in enumerate(proj['units']):
            print(f"->#{unit_id}: {unit['title']} <Checker: {unit['judge']}>")
    print("======== *********** ========")
    f.close()

    # Do the Add task
    if argv[1] == "proj":
        title = input("Enter the new proj title: ")
        obj.append({
            "title": title,
            "units": []
        })

        (Path("database/course") / str(len(obj) - 1)) .mkdir(parents=True, exist_ok=True)
    elif argv[1] == "unit":
        proj_id = input("Enter the index of the target proj: ")
        try:
            proj_id = int(proj_id)
        except ValueError:
            raise InputError(proj_id, "Invalid index")
        if proj_id < 0 or proj_id >= len(obj):
            raise InputError(proj_id, "Index out of range")
        title = input("Enter the new unit title: ")
        judge = input("Enter the judge-method (Empty Means Default): ")
        obj[proj_id]["units"].append({
            "title": title,
            "judge": judge
        })

        unit_file = f"{len(obj[proj_id]['units']) - 1}.json"
        (Path("database/course") / str(proj_id) / unit_file).write_text("[]")
    else:
        assert False

    f = open(course_file, "w")
    json.dump(obj, f)
    f.close()


tasks = {
    "add": _add_op
}

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        print("Expect a Subtask!")
        sys.exit(0)

    if args[1] not in tasks:
        print(f"Unknown Subtask: {args[1]}", end=' ')
        print(f"Expected: {list(tasks.keys())}")
        sys.exit(1)

    try:
        tasks[args[1]](args[1:])
    except ArgvCountError as e:
        print(e)
        sys.exit(2)
    except ArgvWrongError as e:
        print(e)
        sys.exit(3)
    except InputError as e:
        print(e)
        sys.exit(4)
