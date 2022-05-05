#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   grid.py
@Time    :   2022/05/05 10:08:51
@Author  :   Javier G. Visiedo
@Version :   0.0.1
@Contact :   javier.g.visiedo@gmail.com
@License :   (C)Copyright 2021-2022, RedMice
@Desc    :   A grid trading bot written in Python for Uniswap fork decentralized crypto exchanges
'''

from typing import Tuple
from pair import Pair
from decimal import Decimal
from style import style


class Grid():
    """Defines the parameters of the grid based on the passed values

Args:
    lower_limit: Grid minimum price expressed in quote currency
    upper_limit: Grid maximum price expressed in quote currency
    grids: Number of grids to use (levels)
    amount: Max amount available for the bot in quote currency
    pair: Pair to be traded
 
Attributes:
    lower_limit: Grid minimum price expressed in quote currency
    upper_limit: Grid maximum price expressed in quote currency
    grids: Number of grids to use (levels)
    amount: Max amount available for the bot in quote currency
    pair: Pair to be traded

"""
    def __init__(self,
                 lower_limit: Decimal,
                 upper_limit: Decimal,
                 grids: int,
                 amount: Decimal,
                 pair: Pair):
        self.pair = pair
        self.lower_limit = Decimal(lower_limit)
        self.upper_limit = Decimal(upper_limit)
        self.amount = Decimal(amount)
        self.grids = grids
        self.quote_ammount_per_grid = self.amount / Decimal(grids)
        self.step_ammount = (upper_limit-lower_limit) / (self.grids-1)
        self.prices = self.calculate_grid_prices()

    def __str__(self):
        ba, qa = self.calculate_required_amounts()
        content = \
            f"{self.pair.name} grid parameters\n" +\
            "="*len(f"{self.pair.name} grid parameters") + "\n" +\
            f"Lower limit price: {round(self.lower_limit, 2)} {self.pair.token1.symbol}\n" +\
            f"Upper limit price: {round(self.upper_limit, 2)} {self.pair.token1.symbol}\n" +\
            f"Quantity per grid: {round(self.quote_ammount_per_grid, 2)} {self.pair.token1.symbol}\n" +\
            f"Requires around {round(ba, 2)} {self.pair.token0.name}, and {round(qa, 2)} {self.pair.token1.symbol}\n" +\
            "Grids:\n"
        current_price = self.pair.get_token0_price()
        for price in self.prices[::-1]:
            content += "\t- "
            content += style().RED if current_price < price else style().GREEN
            content += f"{round(price, 2)} "
            content += "SELL" if current_price < price else "BUY"
            content += '\n' + style().RESET

        return content

    def calculate_grid_prices(self) -> list[Decimal]:
        return [(self.lower_limit + Decimal(self.step_ammount*i)) for i in range(self.grids)]

    def calculate_required_amounts(self) -> Tuple[Decimal, Decimal]:
        current_price = self.pair.get_token0_price()
        base_amount = Decimal(0)
        quote_amount = Decimal(0)
        for price in self.prices:
            if price <= current_price:
                quote_amount += self.quote_ammount_per_grid
            else:
                base_amount += self.quote_ammount_per_grid / current_price
        return base_amount, quote_amount
