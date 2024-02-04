import sys


def eprint(*_args, **kwargs):
    print(*_args, file=sys.stderr, **kwargs)


def prompt_to_stderr(prompt):
    print(prompt, file=sys.stderr, end="\n")
    return input()
