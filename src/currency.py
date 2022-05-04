#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   currency.py
@Time    :   2022/04/24 22:54:11
@Author  :   Javier G. Visiedo
@Version :   0.0.1
@Contact :   javier.g.visiedo@gmail.com
@License :   (C)Copyright 2021-2022, RedMice
@Desc    :   None
'''

import json
import sys
from os import path

from web3 import Web3

from token_list import TokenList

CURRENT_DIR = path.dirname(__file__)

class Token():
    def __init__(self, w3, token_id):
        tl = TokenList()
        self.address = tl.validate_token_address(token_id)
        try:
            with open(CURRENT_DIR + "/abi/erc20.json", encoding="utf-8") as f:
                self.abi = json.load(f)
            self.contract = w3.eth.contract(self.address, abi=self.abi)
        except OSError as e:
            print(f"\tCould not load token abi: {str(e)}", file=sys.stderr)
            sys.exit(1)
        if self.address not in tl.tokens_by_address:
            tl.add_custom_token(
                self.address,
                self.contract.functions.name().call(),
                self.contract.functions.symbol().call(),
                self.contract.functions.decimals().call(),
                w3.eth.chain_id)
        self.name = tl.tokens_by_address[self.address]["name"]
        self.symbol = tl.tokens_by_address[self.address]["symbol"]
        self.decimals = tl.tokens_by_address[self.address]["decimals"]
        self.chain_id = tl.tokens_by_address[self.address]["chainId"]

    def get_allowance(self, swaper_address):
        return self.contract.functions.allowance(self.address,
            swaper_address).call()

    def print_token_info(self, heading=None):
        if heading is not None:
            print(heading)
            print("="*len(heading))
        print(f"{self.name} / {self.symbol}")
        print(f"Contract: {self.address}")
        print(f"Decimals: {self.decimals}\n")
