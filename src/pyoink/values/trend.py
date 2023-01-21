from pyoink.values.box import Box, Direction

class Trend:
  def __init__(self, columns: list[int], boxes: list[Box], direction: Direction):
    self.columns: list[int] = columns
    self.boxes: list[Box] = boxes
    self.direction: Direction = direction

  def getBoxForColumn(self, column_index):
    data = dict(zip(self.columns, self.boxes))
    if column_index in data:
      return data[column_index]
    return None
    
  def __str__(self):
    boxes = [str(box.price) for box in self.boxes]
    direction = ("DOWN", "UP")[self.direction.value]
    return f"Trend -> direction: {direction} | columns: {self.columns} | boxes = [{', '.join(boxes)}]"  