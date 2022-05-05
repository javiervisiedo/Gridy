#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   wallet.py
@Time    :   2022/05/05 09:38:02
@Author  :   Javier G. Visiedo
@Version :   0.0.1
@Contact :   javier.g.visiedo@gmail.com
@License :   (C)Copyright 2021-2022, RedMice
@Desc    :   A grid trading bot written in Python for Uniswap fork decentralized crypto exchanges
'''

from decimal import Decimal
from currency import Token
from web3 import Web3

class Wallet():
    def __init__(self, w3, address, private_key):
        self.w3 = w3
        self.address = address
        self.private_key = private_key

    def get_token_balance(self, token: Token) -> Decimal:
        return Decimal(token.contract.functions.balanceOf(self.address).call() 
               / (10 ** token.decimals))

    def get_eth_balance(self) -> Decimal:
        return Decimal(self.w3.fromWei(
            self.w3.eth.get_balance(self.address),
            'ether'))