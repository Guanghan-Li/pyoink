from datetime import datetime
import pytz, itertools
from pyoink.values.price import Price

class Prices:
  def __init__(self, symbol, data: list[Price]):
    self.prices: list[Price] = sorted(data, key=lambda price: price.date)
    if len(data) > 0:
      self.start_date = data[0].date
      self.end_date = data[-1].date
    else:
      self.start_date = datetime.now()
      self.end_date = datetime.now()
    self.symbol = symbol.replace(".", "_")
    self.amount = len(data)

  def __len__(self):
    return self.amount

  @property
  def pretty_start_date(self) -> str:
    return self.start_date.strftime("%Y-%m-%d")
  
  @property
  def pretty_end_date(self) -> str:
    return self.end_date.strftime("%Y-%m-%d")

  @property
  def pretty_date_range(self) -> str:
    return self.pretty_start_date + "-" + self.pretty_end_date

  def __str__(self):
    start_date = self.start_date.strftime("%Y-%m-%d")
    end_date = self.end_date.strftime("%Y-%m-%d")
    return f"{self.symbol} -> amount: {self.amount} | start_date: {start_date} | end_date: {end_date}"

  @staticmethod
  def fromDict(symbol, data):
    prices = []
    for p in data:
      price = Price.fromDict(symbol, p)
      prices.append(price)
    
    return Prices(symbol, prices)

  @property
  def empty(self):
    return len(self.prices) == 0

  def toDict(self):
    output = []
    for price in self.prices:
      output.append(price.toDict())
    return output

  def toDict2(self):
    output = []
    for price in self.prices:
      output.append(price.toDict2())
    return output
  
  def toSimpleDict(self):
    output = [price.simpleDict() for price in self.prices]
    return output

  def amountOfYears(self):
    return len(self.splitByYear())

  def amountOfMonths(self):
    return len(self.splitByMonth())

  def amountOfWeeks(self):
    return len(self.splitByWeek())

  def splitByWeek(self):
    def groupFunc(price: Price):
      #return price.date.isocalendar().week
      return (self.end_date - price.date).days // 8
    groups = itertools.groupby(self.prices, key=groupFunc)
    return [Prices(self.symbol, list(group[1])) for group in groups]

  def splitByMonth(self) -> list['Prices']:
    def groupFunc(price: Price):
      return (price.date.year, price.date.month)
    
    groups = itertools.groupby(self.prices, key=groupFunc)
    return [Prices(self.symbol, list(group[1])) for group in groups]

  def splitByYear2(self) -> list['Prices']:
    def groupFunc(price: Price):
      days = (self.end_date - price.date).days
      return days // 366
    
    groups = itertools.groupby(self.prices, key=groupFunc)
    prices = [Prices(self.symbol, list(group[1])) for group in groups]
    return [price for price in prices if price.amount >= 252]
  
  def chunk(self, data, arr_size=252):
    arr_range = iter(data)
    return iter(lambda: tuple(itertools.islice(arr_range, arr_size)), ())


  def splitByYear(self) -> list['Prices']:
    prices = self.prices[::-1]
    groups = self.chunk(prices)
    return [Prices(self.symbol, list(group)[::-1]) for group in groups if len(group) >= 252][::-1]
  
  def get(self, from_index, to_index=-1):
    return Prices(self.symbol, self.prices[from_index:to_index])
  
  def getFromDate(self, from_date=None):
    if from_date != None:
      new_prices = [price for price in self.prices if price.date <= from_date]
    else:
      new_prices = self.prices

    return new_prices

  def getLastYears(self, amount, from_date=None) -> 'Prices':
    new_prices = self.getFromDate(from_date=from_date)

    output = []
    prices = Prices(self.symbol, new_prices).splitByYear()
    for i in range(-1, (amount+1)*-1, -1):
      output += prices[i].prices
    
    return Prices(self.symbol, output)

  def canGetYears(self, amount_of_years, from_date=None):
    new_prices = self.getFromDate(from_date=from_date)
    prices = Prices(self.symbol, new_prices).splitByYear()
    return len(prices) >= amount_of_years
  
  def getBefore(self, date: datetime) -> 'Prices':
    date = self.makeDateGood(date)
    new_prices = [price for price in self.prices if self.makeDateGood(price.date) <= date]
    return Prices(self.symbol, new_prices)

  def makeDateGood(self, date):
    return datetime(date.year, date.month, date.day)

  def splitAt(self, date: datetime):
    date = self.makeDateGood(date)
    before_prices: list[Price] = [price for price in self.prices if self.makeDateGood(price.date) <= date]
    after_prices: list[Price] = [price for price in self.prices if self.makeDateGood(price.date) > date]
    return before_prices, after_prices


  def stockSplit(self, new_rate, old_rate, date):
    before_prices, after_prices = self.splitAt(date)
    adjusted_prices = [price.stockSplit(new_rate, old_rate) for price in before_prices]
    return adjusted_prices + after_prices

  def stockReverseSplit(self, new_rate, old_rate, date):
    before_prices, after_prices = self.splitAt(date)
    adjusted_prices = [price.stockReverseSplit(new_rate, old_rate) for price in before_prices]
    return adjusted_prices + after_prices

    
