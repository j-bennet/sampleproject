# -*- coding: utf-8
import urllib
import csv


class Portfolio(object):
    """A simple stock portfolio

    >>> p = Portfolio()
    >>> p.cost()
    0.0

    >>> p.buy("IBM", 100, 176.48)
    >>> p.cost()
    17648.0

    >>> p.buy("HPQ", 100, 36.15)
    >>> p.cost()
    21263.0

    """

    urllib = urllib

    def __init__(self, *stocks):
        # stocks is a list of lists:
        #   [[name, shares, price], ...]
        self.stocks = []
        for name, shares, price in stocks:
            self.stocks.append([name, shares, price])

    def buy(self, name, shares, price):
        """Buy `name`: `shares` shares at `price`."""
        self.stocks.append([name, shares, price])

    def cost(self):
        """What was the total cost of this portfolio?"""
        amt = 0.0
        for name, shares, price in self.stocks:
            amt += shares * price
        return amt

    def sell(self, name, shares):
        """Sell some number of shares of `name`."""
        stocks = []
        for idx, holding in enumerate(self.stocks):
            if holding[0] == name:
                if holding[1] < shares:
                    raise ValueError("Not enough shares")
                holding[1] -= shares
                if holding[1]:
                    stocks.append(holding)
                break
        else:  # pragma: no cover
            raise ValueError("You don't own that stock")

        self.stocks = stocks

    #(((value)))
    def current_prices(self):
        """Return a dict mapping names to current prices."""
        url = "http://finance.yahoo.com/d/quotes.csv?f=sl1&s="
        url += ",".join(sorted(s[0] for s in self.stocks))
        data = self.urllib.urlopen(url)
        return { sym: float(last) for sym, last in csv.reader(data) }

    def value(self):
        """Return the current value of the portfolio."""
        prices = self.current_prices()
        total = 0.0
        for name, shares, _ in self.stocks:
            total += shares * prices[name]
        return total
    #(((end)))
