# src/utils.py
# plan to use later  on the code base for now raw sql will follow

def kb(n: int) -> int:
    try:
        return n * 1024
    except TypeError:
        raise TypeError("Input must be an integer")


def mb(n: int) -> int:
    try:
        return n * 1024 * 1024
    except TypeError:
        raise TypeError("Input must be an integer")


def gb(n: int) -> int:
    try:
        return n * 1024 * 1024 * 1024
    except TypeError:
        raise TypeError("Input must be an integer")


def bytes_to_gb(size_bytes: int) -> float:
    try:
        return size_bytes / (1024 ** 3)
    except TypeError:
        raise TypeError("Input must be an integer")
