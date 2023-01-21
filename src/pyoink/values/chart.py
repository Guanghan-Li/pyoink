from pyoink.values.column import Box, Column, Direction
from pyoink.values.trend import Trend

class Chart:
  def __init__(self, symbol: str, box_size: float, reversal: int):
    self.symbol = symbol
    self.box_size = box_size
    self.reversal = reversal
    self.columns: list[Column] = [Column(Direction.down, self.box_size)]
    self.trends: list[Trend] = []

  @staticmethod
  def between(price, num1, num2):
    return price >= num1 and price < num2

  @staticmethod
  def getBoxSize(price: float):
    if price < 0.25:
      return 0.0625
    elif Chart.between(price, 0.25, 1.00):
      return 0.125
    elif Chart.between(price, 1.00, 5.00):
      return .25
    elif Chart.between(price, 5.00, 20.00):
      return .5
    elif Chart.between(price, 20.00, 100.00):
      return 1.0
    elif Chart.between(price, 100.00, 200.00):
      return 2.0
    elif Chart.between(price, 200.00, 500.00):
      return 4.0
    elif Chart.between(price, 500.00, 1000.00):
      return 5.0
    elif Chart.between(price, 1000.00, 25000.00):
      return 50.0
    elif price >= 25000:
      return 500.0

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
      last_box = self.last_box
      f = Box(last_box.price, direction=opposite_box.direction, box_size=self.box_size).next()
      new_column = Column(self.last_direction.opposite(), self.box_size, boxes=[f])
      new_column.addBox(opposite_box)
      self.columns.append(new_column)
      if len(new_column.boxes) < self.reversal:
        raise Exception("New Column too small")
    else:
      self.last_column.addBox(box)

  def generate(self, price_data: list[dict[str, float]]) -> 'Chart':
    for price in price_data:
      self.addPrice(price)
    
    return self

  def findHighestColumn(self, indexes) -> int:
    columns = []

    if indexes == [0]:
      indexes = [0,1]

    for index in indexes:
      col = self.columns[index]
      if col.direction == Direction.down:
        continue

      columns.append((index, col))
    
    if not columns:
      raise Exception("ERROR -> findHighestColumn")
      return None

    columns.sort(key=lambda data: data[1].highest_box.price)
    return columns[-1][0]


  def findLowestColumn(self, indexes) -> int:
    columns = []

    for index in indexes:
      col = self.columns[index]
      if col.direction == Direction.up:
        continue

      columns.append((index, col))
  
    if not columns:
      raise Exception("ERROR -> findLowestColumn")
      return None

    columns.sort(key=lambda data: data[1].lowest_box.price)
    return columns[0][0]

  def getIncFunction(self, direction: Direction):
    if direction == Direction.up:
      return self.findHighestColumn
    elif direction == Direction.down:
      return self.findLowestColumn

  def canChangeTrend(self, direction: Direction, current_column: Column, next_box: Box) -> bool:
    if direction == Direction.up:
      return current_column.lowest_box <= next_box
    else:
      return current_column.highest_box >= next_box


  def switchTrend(self, current_trend: Trend) -> Trend:
    findStart = self.getIncFunction(current_trend.direction)
    start = findStart(current_trend.columns)
    if start is None:
      raise Exception("THIS FAILED")

    column = self.columns[start]
    if current_trend.direction == Direction.up:
      start_box = column.highest_box.next()
    else:
      start_box = column.lowest_box.next()
    new_trend = Trend([start,start+1], [start_box], current_trend.direction.opposite())
    return new_trend

  def incrementTrend(self, current_trend: Trend, data: tuple[Column, int]):
    current_column, index = data
    next_trend_box = self.getTrendColumnBox(current_trend.direction, current_trend.boxes[-1])
    can_change = self.canChangeTrend(current_trend.direction, current_column, next_trend_box)
    if can_change:
      current_trend = self.switchTrend(current_trend)
      return current_trend, True
    else:
      current_trend.boxes.append(next_trend_box)
      current_trend.columns.append(index)
      return current_trend, False

  def generateTrends(self):
    trends = []
    start = 0
    start_box = self.columns[0].lowest_box.next()

    current_trend = Trend([start], [start_box], Direction.up)
    is_end = False
    while not is_end:
      for index in range(start+1, len(self.columns)+1):
        if index == len(self.columns):
          is_end = True
          break

        col: Column = self.columns[index]

        old_trend = current_trend
        current_trend, is_change = self.incrementTrend(current_trend, (col, index))
        if is_change:
          trends.append(old_trend)
          start = current_trend.columns[0]
          break
    trends.append(current_trend)
    self.trends = trends
    return trends

  def getGrid(self):
    width = len(self.columns)
    highest_box: Box = Box(0.0, direction=Direction.down)
    lowest_box: Box = Box(1_000.0, direction=Direction.down)

    for col in self.columns:
      if col.lowest_box < lowest_box:
        lowest_box = col.lowest_box
      if col.highest_box > highest_box:
        highest_box = col.highest_box

    height = highest_box.distance(lowest_box) + 4

    grid = []
    for i in range(height):
      grid.append([' ']*width)

    for x, col in enumerate(self.columns):
      char = ('X', "O")[col.direction == Direction.down]

      for box in col.boxes:
        y = highest_box.distance(box)
        grid[y+1][x] = char
      
      for t in self.trends:
        dir_char = (u'\u27CB', u'\u27CD')[t.direction == Direction.down]
        box = None
        if x in t.columns:
          box = t.getBoxForColumn(x)
          if not box:
            continue
          offset = (1,-1)[t.direction == Direction.down]
          y = highest_box.distance(box)
          grid[y][x] = dir_char

    
    return grid

  def getTrendColumnBox(self, direction: Direction, box: Box):
    box_type = ("highest", "lowest")[direction == Direction.up]
    if direction == Direction.down:
      out =  box.dec()
      action = "dec"
    elif direction == Direction.up:
      out = box.inc()
      action = "inc"

    #print("TREND", action, direction, box.direction, box.price, out.price)

    return out

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


