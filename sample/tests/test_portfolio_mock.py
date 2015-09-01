# -*- coding: utf-8
import mock
import unittest
from StringIO import StringIO
from sample.portfolio import Portfolio


class PortfolioValueTest(unittest.TestCase):
    def _makePortfolio(self):
        p = Portfolio()
        p.buy('IBM', 100, 120.0)
        p.buy('HPQ', 100, 30.0)
        return p

    def test_value(self):
        p = self._makePortfolio()
        with mock.patch('urllib.urlopen') as urlopen:
            fake_yahoo = StringIO('"IBM",140\n"HPQ",32\n')
            urlopen.return_value = fake_yahoo
            self.assertEqual(p.value(), 17200)
            urlopen.assert_called_with(
                'http://finance.yahoo.com/d/quotes.csv?f=sl1&s=HPQ,IBM')
