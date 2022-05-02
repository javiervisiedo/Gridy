#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   config.py
@Time    :   2022/04/23 19:45:14
@Author  :   Javier G. Visiedo
@Version :   1.0
@Contact :   javier.g.visiedo@gmail.com
@License :   (C)Copyright 2021-2022, RedMice
@Desc    :   None
'''

import argparse
import json
import sys
from dataclasses import dataclass
from typing import List
from os import path

CURRENT_DIR = path.dirname(__file__)

@dataclass
class Settings():
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        ConfigParser(self.__instance)
    
    tokens: List[str]
    mm_address: str = ""
    mm_private_key: str = ""
    rpc: str = ""
    router_address: str= ""

    gwei_gas: int = 0
    max_tx_fee: int = 0
    slippage: int = 0
    min_liquidity: int = 0

    base_currency: str = ""
    quote_currency: str = ""
    max_amount_available: int = 0
    number_of_grids: int = 0
    min_range_price: float = 0.0
    max_range_price: float = 0.0

    max_sell_tax: int = 0
    min_sell_tax: int = 0

    paper_trade: bool = False

def config_error(msg, is_fatal=False):
    print(msg, file=sys.stderr)
    if is_fatal:
        sys.exit(1)

def ConfigParser(s):
    def load_from_config_or_cmdline(
        key,
        cmd_line_arg,
        valid=lambda x: x == x,
        msg=""
    ):
        param = json_settings.get(key)
        if cmd_line_arg != None:
            param = cmd_line_arg
        if param == None or not valid(param):
            if msg != "":
                print(msg)
            parser.print_usage(sys.stderr)
            sys.exit(1)
        return param

    json_settings = loadSettings()
    parser = loadCMDLineArgs()
    cmd_line_args, unknown = parser.parse_known_args()

    s.mm_address = json_settings.get("metamask_address")
    if s.mm_address == None:
        config_error("Fatal error: a valid Metamask wallet address \
                    must be present in the config file", is_fatal=True)

    s.mm_private_key = json_settings.get("metamask_private_key")
    if s.mm_private_key == None:
        config_error("Fatal error: the Wallet private key \
                    must be present in the config file", is_fatal=True)

    s.rpc = json_settings.get("RPC")
    if s.rpc == None:
        config_error("Fatal error: the RPC end point \
                    must be present in the config file", is_fatal=True)
    
    if json_settings.get("max_sell_tax") != None:
        s.tokens = json_settings.get("tokens")

    s.router_address = json_settings.get("router_address")
    if s.router_address == None:
        config_error("Fatal error: the router address \
                    must be present in teh config file", is_fatal=True)
    
    s.gwei_gas = json_settings.get("GWEI_GAS")
    if s.gwei_gas == None:
        config_error("Fatal error: The GWEI gas value \
                    must be present in the config file", is_fatal=True)

    s.max_tx_fee = json_settings.get("max_tx_fee")
    if s.max_tx_fee == None:
        config_error("Fatal error: the max transaction fee value \
                    must be present in the config file", is_fatal=True)

    s.slippage = json_settings.get("slippage")
    if s.slippage == None:
        config_error("Fatal error: the maximun slippage value \
                    must be present in the config file", is_fatal=True)

    s.min_liquidity = json_settings.get("min_liquidity")
    if s.min_liquidity == None:
        config_error("Fatal error: the minimum liquidity amount \
                    must be present in the config file", is_fatal=True)

    if json_settings.get("max_sell_tax") != None:
        s.max_sell_tax = json_settings.get("max_sell_tax")

    if json_settings.get("min_sell_tax") != None:
        s.min_sell_tax = json_settings.get("min_sell_tax")

    s.base_currency = load_from_config_or_cmdline(
            "base_currency",
            cmd_line_args.base,
            lambda x: x != "",
            "You must specify a base currency"
        )
    
    s.quote_currency = load_from_config_or_cmdline(
            "quote_currency",
            cmd_line_args.quote,
            lambda x: x != "",
            "You must specify a quote currency"
        )

    s.max_amount_available = load_from_config_or_cmdline(
        "max_amount_available", cmd_line_args.amount
    )

    s.number_of_grids = load_from_config_or_cmdline(
        "number_of_grids", cmd_line_args.grids
    )

    s.min_range_price = load_from_config_or_cmdline(
        "min_range_price", cmd_line_args.min_price
    )

    s.max_range_price = load_from_config_or_cmdline(
        "max_range_price", cmd_line_args.max_price
    )

    s.paper_trade = cmd_line_args.paper_trade

def loadSettings():
    try:
        f = open(CURRENT_DIR + "/conf/settings.json", "r")
    except FileNotFoundError as e:
        config_error(f"Fatal error: The config file \
                    '{CURRENT_DIR}/conf/settings.json' could not be found. {str(e)}", 
                    is_fatal=True)
    with f:
        try:
            json_settings = json.load(f)
        except ValueError as e:
            config_error("Syntax error on " \
                        f"'{CURRENT_DIR}/conf/settings.json' config file. {str(e)}", 
                        is_fatal=True)
    return json_settings

def loadCMDLineArgs():
    def validateGrids(g):
        num_grids = int(g)
        if num_grids < 2 or num_grids > 200:
            raise argparse.ArgumentTypeError('invalid number of grids')
        return num_grids

    def validateString(s):
        string_value = str(s)
        if string_value == "":
            raise argparse.ArgumentTypeError(
                'String value cannot be empty')
        return string_value

    parser = argparse.ArgumentParser(
        description='Grid trading bot for crypto decentralized exchanges'
    )
    parser.add_argument(
        '-b', '--base',
        type=validateString,
        help='Contract address for base currency. e.g. \
            "--base 0x7ad7242A99F21aa543F9650A56D141C57e4F6081"'
    )
    parser.add_argument(
        '-q', '--quote',
        type=validateString,
        help='Contract address for quote currency. e.g. \
            "--quote 0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"'
    )
    parser.add_argument(
        '-a', '--amount', type=float, help='Max amount in quote currency \
        available for the bot to trade. e.g. "--ammount 1200.0"'
    )
    parser.add_argument(
        '-g', '--grids',
        type=validateGrids,
        help='Number of grids to setup (2-200). e.g. "--grids 10"'
    )
    parser.add_argument(
        '-m', '--min-price',
        type=float,
        help='Minimum price for the grid range. e.g. "--min-price 10.5"'
    )
    parser.add_argument(
        '-M', '--max-price',
        type=float,
        help='Maximum price for the grid range. e.g. "--min-price 12.3"'
    )
    parser.add_argument(
        '-pt', '--paper-trade',
        action="store_true",
        help="Paper trading; Runs the bot with the options provided without \
            performing any actual trades"
    )
    return parser

settings = Settings()
