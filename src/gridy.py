#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   gridy.py
@Time    :   2022/04/23 12:22:17
@Author  :   Javier G. Visiedo
@Version :   0.0.1
@Contact :   javier.g.visiedo@gmail.com
@License :   (C)Copyright 2021-2022, RedMice
@Desc    :   None
'''

from typing_extensions import Self
from web3 import Web3

from art import banner
from art import red_mice_art as ascii_art
from config import settings
from currency import Token
from router import Router
from style import style
from token_list import TokenList
from w3tx import W3TX
from pair import Pair


class Gridy():

    def __init__(self):
        self.say_hello()
        self.txn = W3TX()
        self.token_list = TokenList()
        self.quote_token = Token(self.txn.w3, settings.quote_currency)
        self.base_token = Token(self.txn.w3, settings.base_currency)
        self.eth = Token(self.txn.w3, 'WBNB')
        #TODO: create list of tokens including base, quote, and all possible
        #base tokens in the chain that could potentially be part of the path
        self.tokens = [self.base_token, self.quote_token, self.eth]
        self.pancake_router = Router(
            self.txn.w3,
            settings.router_address,
            "pancakeswap")
        self.pairs = self.create_pairs()

    def create_pairs(self):
        pairs: dict[str, Pair] = {}
        all_pairs = [(token0, token1) for idx, token0 in
            enumerate(self.tokens) for token1 in self.tokens[idx + 1:]]
        for p in all_pairs:
            pair = Pair(self.txn.w3, self.pancake_router, p[0], p[1])
            pairs[pair.key] = pair
        return pairs

    def say_hello(self):
        print(style().RED + ascii_art + style().RESET)
        print(style().RED + banner + style().RESET)

    def start(self):
        self.quote_token.print_token_info("Quote token")
        self.base_token.print_token_info("Base token")
        for pair in self.pairs.values():
            pair.print_pair_info()

Gridy().start()
