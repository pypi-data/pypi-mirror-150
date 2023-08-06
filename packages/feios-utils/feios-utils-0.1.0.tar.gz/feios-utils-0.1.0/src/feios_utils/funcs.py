# FEI OS useful utils

__all__ = ["out", "outline", "run", "runbatch"]


def out(txt: str):
    print(txt, end="")


def outline(txt: str):
    print(txt, end="\n")


def run(tl: list[str]):
    for line in tl:
        if line.startswith("#"):
            continue
        elif line[:3] == "out":
            if line[3] != " ":
                print("""Input and/or script error:\
                ERROR 001
                There should be a space.
                Execution halted.
                """)
                return 2
            else:
                print(line[4:])
                continue
        elif line[:4] == "exit":
            return 0
        else:
            print("""Input and/or script error:\
            ERROR 002
            No such command
            Execution halted.
            """)
            return 2
    return 0


def runbatch(pof):
    f = open(pof, 'r')
    content = f.readlines()
    ret = run(content)
    return ret

