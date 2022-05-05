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

# TODO: Add support for reading known networks info from
# https://chainid.network/chains.json so we can map network information such as
# chain_id, rpc, native currency, etc. from there

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
from wallet import Wallet
from grid import Grid
import sys


class Gridy():

    def __init__(self):
        self.say_hello()
        self.txn = W3TX()
        self.known_token_list = TokenList()
        self.quote_token = Token(self.txn.w3, settings.quote_currency)
        self.base_token = Token(self.txn.w3, settings.base_currency)
        self.eth = Token(self.txn.w3, 'WBNB')
        #TODO: create list of tokens including base, quote, and all possible
        #base tokens in the chain that could potentially be part of the path
        self.traded_tokens = [self.base_token, self.quote_token]
        self.pancake_router = Router(
            self.txn.w3,
            settings.router_address,
            "pancakeswap")
        self.pairs = self.create_pairs()
        self.my_wallet = Wallet(
            self.txn.w3,
            settings.mm_address,
            settings.mm_private_key)

    def create_pairs(self):
        pairs: dict[str, Pair] = {}
        all_pairs = [(token0, token1) for idx, token0 in
            enumerate(self.traded_tokens) for token1 in self.traded_tokens[idx + 1:]]
        for p in all_pairs:
            pair = Pair(self.txn.w3, self.pancake_router, p[0], p[1])
            pairs[pair.key] = pair
        return pairs

    def say_hello(self):
        print(style().RED + ascii_art + style().RESET)
        print(style().RED + banner + style().RESET)

    def start(self):
        print(self.quote_token)
        print(self.base_token)
        for pair in self.pairs.values():
            print(pair)
        print("Wallet balances")
        print("===============")
        
        print(f"{self.my_wallet.get_eth_balance()} BNB")
        for token in self.traded_tokens:
            print(f"{self.my_wallet.get_token_balance(token)} {token.symbol}")
        traded_pair = self.pairs[self.pancake_router.name + \
                                 ':' + self.base_token.address + \
                                 '-' + self.quote_token.address]
        my_grid = Grid(settings.min_range_price,
                       settings.max_range_price,
                       settings.number_of_grids,
                       settings.max_amount_available,
                       traded_pair)
        print(f"\n{my_grid}")
        req_base_amount, req_quote_amount = my_grid.calculate_required_amounts()
        wallet_base_balance = self.my_wallet.get_token_balance(self.base_token)
        wallet_quote_balance = self.my_wallet.get_token_balance(self.quote_token)
        current_price = traded_pair.get_token0_price()
        total_required_amount = req_base_amount*current_price + req_quote_amount
        total_available_balance = wallet_base_balance*current_price + wallet_quote_balance
        if total_required_amount > total_available_balance:
            print(style().RED + "Not enough balance to start the bot\n" + style().RESET)
            sys.exit(1)
        if wallet_base_balance < req_base_amount:
            print(f"You need {req_base_amount-wallet_base_balance} additional \
                    {self.base_token.symbol} to start the bot. \
                    Do you want to buy it now for \
                    {(req_base_amount-wallet_base_balance)*current_price} \
                    {self.quote_token.symbol}? [y/n]")
        if wallet_quote_balance < req_quote_amount:
            print(f"You need {req_quote_amount-wallet_quote_balance} additional \
                    {self.quote_token.symbol} to start the bot. \
                    Do you want to swap  \
                    {(req_quote_amount-wallet_quote_balance)/current_price} \
                    {self.base_token.symbol} to cover the difference? [y/n]")


Gridy().start()
