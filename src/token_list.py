#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   token-list.py
@Time    :   2022/04/29 13:16:01
@Author  :   Javier G. Visiedo
@Version :   0.0.1
@Contact :   javier.g.visiedo@gmail.com
@License :   (C)Copyright 2021-2022, RedMice
@Desc    :   None
'''

import json
import sys
from os import path

import requests
from web3 import Web3

from config import settings
from style import style

CURRENT_DIR = path.dirname(__file__)

BSC_MAINNET = 56
BSC_TESTNET = 97

class TokenList():
    """Singelton object holding information about all known token

    TokenList is a singelton object, it gets constructed and initialized
    just once, and holds information about the known tokens, both the trusted
    tokens loaded from trusted sources, and those added by the user over time.

    When the user specifies a new token to be traded, which is unknown, the
    initializer fetches the token information from the blockchain, and stores
    it in the user defined token list.

    Attributes:
        __instance: singelton object
        __initialized: bool indicating if the object is already initialized
        tokens_by_symbol: dictionary of all known tokens keyed by symbol
        tokens_by_address: dictionary of all known tokens keyed by ETH address
    """

    __instance = None
    __initialized = False

    """Initializes the token dictionaries from the specified sources
    """
    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self.tokens_by_symbol = {}
        self.tokens_by_address = {}
        print ("Loading default token list", end=' ')
        for url in settings.tokens:
            print (".", end='')
            raw_token_list = self.load_token_list_from_url(url)
            if raw_token_list is not None:
                self.init_token_list(json.loads(raw_token_list))
        print(style().GREEN + " [OK]" + style().RESET)
        try:
            print ("Loading user defined token list .", end='')
            with open(CURRENT_DIR + "/conf/BSC-user-tokenlist.json", mode="r",
                encoding="utf-8") as user_list_file:
                self.init_token_list(json.load(user_list_file))
                print(style().GREEN + " [OK]" + style().RESET)
        except OSError as e:
            print(style().RED + " [NOK]" + style().RESET)
            print(f"\tCould not load user token list {str(e)}",
                file=sys.stderr)
        self.validate_config_pair()

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def load_token_list_from_url(self, url) -> str:
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
                    chainId = token["chainId"],
                    decimals = token["decimals"]
                )
                self.tokens_by_address[token["address"]] = dict(
                    name = token["name"],
                    symbol = token["symbol"],
                    chainId = token["chainId"],
                    decimals = token["decimals"]
                )

    def validate_token_address(self, token_id):
        if not Web3.isAddress(token_id):
            if token_id not in self.tokens_by_symbol:
                print(f"Fatal error: Could not find token symbol {token_id}. \
                       Please provide the token address instead", file=sys.stderr)
                sys.exit(1)
            token_id = self.tokens_by_symbol[token_id]["address"]
        return Web3.toChecksumAddress(token_id)

    def validate_config_pair(self):
        settings.base_currency = self.validate_token_address(settings.base_currency)
        settings.quote_currency = self.validate_token_address(settings.quote_currency)

    def add_custom_token(self, address, name, symbol, decimals, chain_id):
        print (f"Adding {name} to known tokens list", end=" ")
        try:
            with open(CURRENT_DIR + "/conf/BSC-user-tokenlist.json", "r+") as user_list_file:
                token_list = json.load(user_list_file)
                token_list["tokens"].append({
                    "name": name,
                    "symbol": symbol,
                    "address": address,
                    "chainId": chain_id,
                    "decimals": decimals
                })
                user_list_file.seek(0)
                json.dump(token_list, user_list_file, indent=4)
                print(style().GREEN + " [OK]" + style().RESET)

        except OSError as e:
            print(style().RED + " [NOK]" + style().RESET)
            print(f"\tCould not load user token list {str(e)}",
                file=sys.stderr)
