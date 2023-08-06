from typing import Any


class R:
    def __init__(self, path: str) -> None:
        pass

    def sd(self, childpath: str) -> str:
        pass

    def context(self) -> str:
        pass

    def root(self, childpath: str) -> str:
        pass

    def res(self, childpath: str) -> str:
        pass

class Device:

    def display(self) -> Any:
        pass


    def name(self) -> str:
        pass

    def brand(self) -> str:
        pass

    def model(self) -> str:
        pass

    def sdk(self) -> str:
        pass

    def version(self) -> str:
        pass


    def ip(self) -> str:
        pass

    def currentAppInfo(self) -> Any:
        pass




