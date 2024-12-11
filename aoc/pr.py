import pyperclip
from rich import print


def pr(s):
    print(s)
    pyperclip.copy(str(s))
