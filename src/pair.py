#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   pair.py
@Time    :   2022/05/04 10:20:14
@Author  :   Javier G. Visiedo
@Version :   0.0.1
@Contact :   javier.g.visiedo@gmail.com
@License :   (C)Copyright 2021-2022, RedMice
@Desc    :   A grid trading bot written in Python for Uniswap fork decentralized crypto exchanges
'''

from tarfile import CompressionError
from currency import Token
from web3 import Web3
from decimal import Decimal

from router import Router

class Pair():
    """Represents a pair of tokens in a block chain

    Args:
        w3 (Web3): Web3 connection
        token0 (Token): First token in the pair
        token1 (Token): Second token in the pair

    Attributes:
        key (string): Internal pair key: 'chain_id-token0.address-token1.address

    Raises:
        ValueError: If token0.chain_id is not equal to token1.chain_id
    """
    w3: Web3
    token0: str
    token1: str
    router: Router
    key: str
    name: str

    def __init__(self, w3: Web3, router: Router, token0: Token, token1: Token) -> None:
        if token0.chain_id is not token1.chain_id:
            raise ValueError("Both tokens must have the same `chain_id`")
        self.w3 = w3
        self.token0 = token0
        self.token1 = token1
        self.router = router
        self.key, self.name = self.compose_pair_ids()
    
    def __str__(self):
        return self.name + "\n" +\
               "="*len(self.name) + "\n" +\
               f"{self.token0.symbol} price: \
               {round(self.get_token0_price(), 3)} {self.token1.symbol}\n" +\
               f"{self.token1.symbol} price: \
               {round(self.get_token1_price(), 3)} {self.token0.symbol}\n"

    def compose_pair_ids(self):
        key = self.router.name + \
        ':' + self.token0.address + \
        '-' + self.token1.address
        name = self.token0.symbol + self.token1.symbol
        return key,name

    def getOutputfromETHtoToken(self, amount=1):
        token0_call = self.router.functions.getOutputfromETHtoToken(
            self.token0.address,
            Web3.toWei(amount, 'ether'),
            ).call()
        token1_call = self.router.functions.getOutputfromETHtoToken(
            self.token1.address,
            Web3.toWei(amount, 'ether'),
            ).call()
        return [
            (token0_call[0], token0_call[1]),
            (token1_call[0], token1_call[1])
        ]

    def getOutputfromTokentoETH(self, amount=1):
        token0_call = self.router.contract.functions.getOutputfromTokentoETH(
            self.token0.address,
            Web3.toWei(amount, 'ether'),
            ).call()
        token1_call = self.router.contract.functions.getOutputfromTokentoETH(
            self.token1.address,
            Web3.toWei(amount, 'ether'),
            ).call()
        return [
            (token0_call[0], token0_call[1]),
            (token1_call[0], token1_call[1])
        ]

    def get_token0_price(self, amount=1) -> Decimal:
        swap_path = [self.token0.address, self.token1.address]
        quote = self.router.contract.functions.getAmountsOut(
            amount*(10**self.token0.decimals),
            swap_path).call()
        return Decimal(quote[-1]/(10**self.token1.decimals))

    def get_token1_price(self, amount=1) -> Decimal:
        swap_path = [self.token1.address, self.token0.address]
        quote = self.router.contract.functions.getAmountsOut(
            amount*(10**self.token1.decimals),
            swap_path).call()
        return Decimal(quote[-1]/(10**self.token0.decimals))

    def get_price_of(self, token, amount=1):
        return (self.get_token0_price(amount)
                if token is self.token0.address
                else self.get_token1_price)
