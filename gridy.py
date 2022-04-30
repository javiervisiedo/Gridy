#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   gridy.py
@Time    :   2022/04/23 12:22:17
@Author  :   Javier G. Visiedo 
@Version :   1.0
@Contact :   javier.g.visiedo@gmail.com
@License :   (C)Copyright 2021-2022, RedMice
@Desc    :   None
'''

from config import settings
from style import style
from art import red_mice_art as ascii_art
from art import banner
from w3tx import W3TX
from currency import Token
from router import Router
from web3 import Web3
from token_list import TokenList

class Gridy():

    def __init__(self):
        self.sayHello()
        self.txn = W3TX()
        self.token_list = TokenList()
        self.quote_token = Token(self.txn.w3, settings.quote_currency)
        self.base_token = Token(self.txn.w3, settings.base_currency)
        self.router = Router(self.txn.w3, settings.router_address)


    def sayHello(self):
        print(style().RED + ascii_art + style().RESET)
        print(style().RED + banner + style().RESET)

    def Start(self):
        print(f"{self.quote_token.name} {self.quote_token.symbol} {self.quote_token.decimals}")
        print(self.quote_token.get_allowance(settings.base_currency))
        print(f"{self.base_token.name} {self.base_token.symbol} {self.base_token.decimals}")
        print(self.base_token.get_allowance(settings.quote_currency))
        print(Web3.fromWei(
            self.router.getPrice(
                self.quote_token.address, 
                self.base_token.address
            )[1],
            'ether'
            )
        )
        
Gridy().Start()
