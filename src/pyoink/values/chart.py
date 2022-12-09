from pyoink.values.column import Box, Column, Direction

class Chart:
  def __init__(self, symbol: str, box_size: float, reversal: int):
    self.symbol = symbol
    self.box_size = box_size
    self.reversal = reversal
    self.columns: list[Column] = [Column(Direction.down, self.box_size)]

  @property
  def last_column(self) -> Column:
    return self.columns[-1]

  @property
  def last_box(self) -> Box:
    return self.columns[-1].last_box

  @property
  def last_direction(self) -> Direction:
    return self.last_column.direction
  
  def addPrice(self, raw_price: dict[str, float]):
    if len(self.columns) == 1 and self.columns[0].amount == 0:
      box1 = Box(Box.roundDown(raw_price['h'], self.box_size), Direction.down, self.box_size)
      box2 = Box(raw_price['l'], Direction.down, self.box_size)
      self.columns[0].addBox(box1)
      self.columns[0].addBox(box2)
      return
    box = Box(raw_price, self.last_direction, self.box_size)
    opposite_box = Box(raw_price, direction=self.last_direction.opposite(), box_size=self.box_size)
    distance = opposite_box.distance(self.last_box)
    if distance >= self.reversal:
      new_column = Column(self.last_direction.opposite(), self.box_size, boxes=[])
      new_column.addBox(opposite_box)
      self.columns.append(new_column)
    else:
      self.last_column.addBox(box)

  def generate(self, price_data: list[dict[str, float]]) -> 'Chart':
    for price in price_data:
      self.addPrice(price)
    
    return self
  
  def getGrid(self):
    width = len(self.columns)
    highest_box: Box = Box(0.0, direction=Direction.down)
    lowest_box: Box = Box(1_000.0, direction=Direction.down)

    for col in self.columns:
      if col.lowest_box < lowest_box:
        lowest_box = col.lowest_box
      if col.highest_box > highest_box:
        highest_box = col.highest_box

    height = highest_box.distance(lowest_box) + 1

    grid = []
    for i in range(height):
      grid.append([' ']*width)

    for x, col in enumerate(self.columns):
      char = ('X', "O")[col.direction == Direction.down]

      for box in col.boxes:
        y = highest_box.distance(box)
        grid[y][x] = char
    
    return grid

  def print(self):
    grid = self.getGrid()
    for row in grid:
      print(' '.join(row))
  
  def toHtml(self, file_name="webpage.html"):
    grid: list[list[str]] = self.getGrid()
    style = """
      body, html {
        background-color: black;
      }
      table{
        border-collapse:collapse;
        border:0px solid #fff;
        }

        table td {
        border:0px solid #fff;
        }
    """
    webpage = f"<html><head><style>{style}</style><title>{self.symbol} PNF</title></head><body><table>"
    for row in grid:
      webpage += "<tr>"
      html_row = []
      for char in row:
        color = ('red', "green")[char == 'X']
        cell = f"<td width='5px' height='5px' style='color: {color}'>{char}</td>"
        html_row.append(cell)
      webpage += ''.join(html_row) + "</tr>"
    webpage += "</table></body></html>"

    with open(file_name, "w") as f:
      f.write(webpage)


