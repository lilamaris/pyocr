RawPos = tuple[int, int]


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Pos(x={self.x}, y={self.y})"


class Rectangle:
    def __init__(self, p1: Position, p2: Position) -> None:
        if p1.x == p2.x or p1.y == p2.y:
            raise ValueError(f"Position overlap: {p1}, {p2}")

        is_p1_left = True if p1.x < p2.x else False
        is_p1_bottom = True if p1.y < p2.y else False

        self.left = p1.x if is_p1_left else p2.x
        self.right = p2.x if is_p1_left else p1.x
        self.bottom = p1.y if is_p1_bottom else p2.y
        self.top = p2.y if is_p1_bottom else p1.y

        self.height = self.top - self.bottom
        self.width = self.right - self.left

    def __repr__(self) -> str:
        return f"Rectangle(left={self.left}, top={self.top}, right={self.right}, bottom={self.bottom})"


def rect_factory(pairs: dict[str, tuple[RawPos, RawPos]]):
    return {
        key: Rectangle(Position(c1[0], c1[1]), Position(c2[0], c2[1]))
        for key, (c1, c2) in pairs.items()
    }


recipe_roi_rect = rect_factory(
    {
        "order_number": ((862, 288), (1120, 344)),
        "price": ((878, 531), (1041, 600)),
        "orderer": ((69, 1331), (219, 1404)),
        "address": ((61, 1415), (1100, 1535)),
        "contact": ((69, 1557), (355, 1621)),
        "product": ((301, 2214), (1090, 2350)),
    }
)
