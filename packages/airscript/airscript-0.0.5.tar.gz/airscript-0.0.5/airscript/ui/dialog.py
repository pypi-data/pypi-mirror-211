from typing import Any


def toast(msg: str, duration: int = 2, x=-1, y=-1) -> None:
    pass


def alert(msg: str, submit: str) -> None:
    pass


class confirm:
    def __init__(self, msg: str):
        pass

    def title(self, msg: str) -> 'confirm':
        pass

    def submit(self, msg: str) -> 'confirm':
        pass

    def cancel(self, msg: str) -> 'confirm':
        pass

    def close(self):
        pass

    def show(self, pyfun: Any):
        pass


class promat:
    def __init__(self, msg: str):
        pass

    def title(self, msg: str) -> 'promat':
        pass

    def value(self, msg: str) -> 'promat':
        pass

    def hint(self, msg: str) -> 'promat':
        pass

    def submit(self, msg: str) -> 'promat':
        pass

    def cancel(self, msg: str) -> 'promat':
        pass

    def close(self):
        pass

    def show(self, pyfun: Any):
        pass




