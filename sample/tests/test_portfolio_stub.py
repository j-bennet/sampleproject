# -*- coding: utf-8
import unittest
from sample.portfolio import Portfolio
from StringIO import StringIO


class FakeUrllib(object):
    """
    Stub of urllib
    """
    def urlopen(self, url):
        return StringIO('"IBM",140\n"HPQ",32\n')


class PortfolioValueTest(unittest.TestCase):
    def stub_current_prices(self):
        return {'IBM': 140.0, 'HPQ': 32.0}

    def _makePortfolio(self):
        p = Portfolio()
        p.buy('IBM', 100, 120.0)
        p.buy('HPQ', 100, 30.0)

        # Replace an actual method with our stub
        # p.current_prices = self.stub_current_prices
        p.urllib = FakeUrllib()

        return p

    def test_value(self):
        p = self._makePortfolio()
        self.assertEqual(p.value(), 17200)

    def test_value_no_stocks(self):
        p = self._makePortfolio()
        p.stocks = []
        self.assertEqual(p.value(), 0)
