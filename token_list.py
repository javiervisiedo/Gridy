#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   token-list.py
@Time    :   2022/04/29 13:16:01
@Author  :   Javier G. Visiedo 
@Version :   1.0
@Contact :   javier.g.visiedo@gmail.com
@License :   (C)Copyright 2021-2022, RedMice
@Desc    :   None
'''

import json
import requests
import sys
from config import settings
from style import style
from config import settings
from web3 import Web3

BSC_MAINNET = 56
BSC_TESTNET = 97

class TokenList():
    __instance = None

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self.tokens_by_symbol = {}
        self.tokens_by_address = {}
        for url in settings.tokens:
            print (f"Loading token list from {url}...")
            raw_token_list = self.load_token_list_from_url(url)
            if raw_token_list != None:
                self.init_token_list(json.loads(raw_token_list))
#        try:
#            with open("conf/BSC-vetted-tokenlist.json", "r") as vetted_list_file:
#                print("Loading vetted token list...")
#                self.init_token_list(json.load(vetted_list_file))
#        except OSError as e:
#            print >> sys.stderr, 
#            "Warining: Could not load vetted token list %s" % str(e)
        
        try:
            with open("conf/BSC-user-tokenlist.json", "r") as user_list_file:
                print ("Loading user defined token list...")
                self.init_token_list(json.load(user_list_file))
        except OSError as e:
            print(f"\tWarining: Could not load user token list {str(e)}", 
                file=sys.stderr)
        self.validate_config_pair()

    def __new__(self, *args, **kwargs):
        if not self.__instance:
            self.__instance = object.__new__(self)
            self.__instance.__initialized = False
        return self.__instance

    def load_token_list_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            print("\t" + style().RED + str(e) + style().RESET, file=sys.stderr)
            return None
        except requests.exceptions.RequestException as e:
            print("\t" + style().RED + e + style().RESET, file=sys.stderr)
            return None

    def init_token_list(self, token_list):
        for token in token_list["tokens"]:
            if token["chainId"] == BSC_MAINNET:
                self.tokens_by_symbol[token["symbol"]] = dict(
                    name = token["name"],
                    address = token["address"],
                    chainID = token["chainId"],
                    decimals = token["decimals"]
                )
                self.tokens_by_address[token["address"]] = dict(
                    name = token["name"],
                    symbol = token["symbol"],
                    chainID = token["chainId"],
                    decimals = token["decimals"]
                )

    def validate_config_pair(self):
        def validate(token_id):
            if not Web3.isAddress(token_id):
                if token_id not in self.tokens_by_symbol:
                    print(f"Fatal error: Could not find token symbol {token_id}. \
                        Please provide the token address instead", file=sys.stderr)
                    sys.exit(1)
                token_id = self.tokens_by_symbol[token_id]["address"]
            return Web3.toChecksumAddress(token_id)

        settings.base_currency = validate(settings.base_currency)
        settings.quote_currency = validate(settings.quote_currency)

    def add_custom_token(self, address, name, symbol, decimals, chainId):
        print ("Adding custom token to known tokens list...")
        try:
            with open("conf/BSC-user-tokenlist.json", "r+") as user_list_file:
                token_list = json.load(user_list_file)
                token_list["tokens"].append({
                    "name": name,
                    "symbol": symbol,
                    "address": address,
                    "chainId": chainId,
                    "decimals": decimals
                })
                user_list_file.seek(0)
                json.dump(token_list, user_list_file, indent=4)

        except OSError as e:
            print(f"\tWarining: Could not load user token list {str(e)}", 
                file=sys.stderr)
