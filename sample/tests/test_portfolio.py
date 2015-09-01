# -*- coding: utf-8
import unittest


class PortfolioTest(unittest.TestCase):

    def _makePortfolio(self, *args, **kwargs):
        from sample.portfolio import Portfolio
        p = Portfolio(*args, **kwargs)
        return p

    def test_ctr(self):
        p = self._makePortfolio()
        self.assertEqual(p.stocks, [])

    def test_buy(self):
        """
        No side effects from 'cost()'
        """
        p = self._makePortfolio(["IBM", 1, 10])
        self.assertEqual(p.stocks, [['IBM', 1, 10]])

    def test_empty(self):
        p = self._makePortfolio()
        self.assertEqual(p.cost(), 0.0)

    def test_buy_one_stock(self):
        p = self._makePortfolio(["IBM", 100, 176.48])
        self.assertEqual(p.cost(), 17648.0)

    def test_buy_two_stocks(self):
        p = self._makePortfolio()
        p.buy("IBM", 100, 176.48)
        p.buy("HPQ", 100, 36.15)
        self.assertEqual(p.cost(), 21263.0)

    def test_sell_all(self):
        p = self._makePortfolio(['IBM', 10, 1])
        p.sell("IBM", 10)
        self.assertEqual(p.stocks, [])

    def test_sell_some(self):
        p = self._makePortfolio(['IBM', 10, 1])
        p.sell("IBM", 1)
        self.assertEqual(len(p.stocks), 1)
        self.assertEqual(p.stocks[0], ['IBM', 9, 1])

    def test_sell_unowned(self):
        p = self._makePortfolio()
        with self.assertRaises(ValueError):
            p.sell("IBM", 10)

    def test_sell_too_many_shares(self):
        p = self._makePortfolio()
        p.buy('IBM', 10, 1)
        with self.assertRaisesRegexp(ValueError, 'Not enough shares'):
            p.sell("IBM", 20)

    def test_bad_input(self):
        p = self._makePortfolio()
        with self.assertRaises(TypeError):
            p.buy("IBM")
