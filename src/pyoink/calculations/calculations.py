import math
from pyoink.values.prices import Prices, Price

class Calculations:
  @staticmethod
  def trueRange(high, low, close):
    first = high - low
    second = abs(high - close)
    third = abs(low - close)
    return max([first, second, third])

  @staticmethod
  def averageTrueRange(prices: Prices, time_period):
    true_ranges = []
    amount_prices = len(prices)-1
    start = amount_prices-time_period
    
    for price in prices.prices[start:]:
      high = price.high
      low = price.low
      close = price.close
      true_ranges.append(Calculations.trueRange(high, low, close))

    return sum(true_ranges) / time_period
  

