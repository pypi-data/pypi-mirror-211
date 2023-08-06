import graphics


# 点击
def click(x: int | graphics.Point, y=None, dur=20) -> None:
    if isinstance(x, graphics.Point):
        point = x
        x = point.x
        y = point.y
    elif y is None:
        raise ValueError("If the first argument is not a Point, both x and y should be provided.")


# 滑动
def slide(x: int, y: int, y1: int, dur=20) -> None:
    pass
