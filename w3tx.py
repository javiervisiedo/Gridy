#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   w3tx.py
@Time    :   2022/04/24 19:14:51
@Author  :   Javier G. Visiedo 
@Version :   1.0
@Contact :   javier.g.visiedo@gmail.com
@License :   (C)Copyright 2021-2022, RedMice
@Desc    :   None
'''

from web3 import Web3
from web3.middleware import geth_poa_middleware
from config import settings

class W3TX():
    def __init__(self):
        self.w3 = self.connect()
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def connect(self):
        return Web3(Web3.HTTPProvider(settings.rpc))
    
    def getLatestBlock(self):
        return self.w3.eth.block_number
