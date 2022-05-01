#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   currency.py
@Time    :   2022/04/24 22:54:11
@Author  :   Javier G. Visiedo 
@Version :   1.0
@Contact :   javier.g.visiedo@gmail.com
@License :   (C)Copyright 2021-2022, RedMice
@Desc    :   None
'''

from web3 import Web3
import json
from token_list import TokenList

class Token():
    def __init__(self, w3, token_id):
        tl = TokenList()
        self.address = token_id
        with open("./abi/" + self.address + ".json") as f:
            self.abi = json.load(f)
        self.contract = w3.eth.contract(self.address, abi=self.abi)
        self.decimals = self.contract.functions.decimals().call()
        self.name = self.contract.functions.name().call()
        self.symbol = self.contract.functions.symbol().call()
        
        if self.address not in tl.tokens_by_address:
            tl.add_custom_token(
                self.address, 
                self.name, 
                self.symbol,
                self.decimals,
                w3.eth.chain_id)

    def get_allowance(self, swaper_address):
        return self.contract.functions.allowance(self.address, 
            swaper_address).call()
