class HuffNode:

    def __init__(self, symbol: str, frequency: float):
        self.symbol = symbol
        self.frequency = frequency

        self.parent = None
        self.left_child = None
        self.right_child = None

    def __str__(self):
        return f"(Symbol={self.symbol}, Frequency={self.frequency})"


class InnerNode:

    def __init__(self, left_child, right_child):
        self.left_child = left_child
        self.right_child = right_child
        self.parent = None

        self.frequency = self.left_child.frequency + self.right_child.frequency





