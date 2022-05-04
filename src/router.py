#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   router.py
@Time    :   2022/04/25 22:41:18
@Author  :   Javier G. Visiedo 
@Version :   0.0.1
@Contact :   javier.g.visiedo@gmail.com
@License :   (C)Copyright 2021-2022, RedMice
@Desc    :   None
'''

from web3 import Web3
import json
from decimal import Decimal
from os import getcwd
from os import path

CURRENT_DIR = path.dirname(__file__)

class Router():
    def __init__(self, w3, router_address, router_name):
        self.address = Web3.toChecksumAddress(router_address)
        with open(CURRENT_DIR + "/abi/IPancakeRouter02.json") as f:
            self.abi = json.load(f)
        self.contract = w3.eth.contract(self.address, abi=self.abi)
        self.name = router_name

    def getPrice(self, base_token, quote_token, amount=1):
        p=[base_token, quote_token]
        return self.contract.functions.getAmountsOut(
            Web3.toWei(Decimal(amount), 'ether'),
            p
        ).call()
