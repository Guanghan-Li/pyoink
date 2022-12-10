from pyoink.values.box import Box, Direction

class Trend:
  def __init__(self, columns: list[int], boxes: list[Box], direction: Direction):
    self.columns: list[int] = columns
    self.boxes: list[Box] = boxes
    self.direction: Direction = direction
    