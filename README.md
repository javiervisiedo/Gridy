# Gridy

Gridy is a trading bot implementing a grid strategy for crypto currencies 
trading at Uniswap derived decentralized exchanges. It was created
as an experimental tool for learning purposes.

## Disclaimer

This software is for educational purposes only. Do not risk money. You are free
to USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHOR ASSUMES NO RESPONSIBILITY FOR
 YOUR TRADING RESULTS.

The bot support a paper trading option to simulate trades and calculate 
potential profit and loss. Please make sure to always start by using this option
starting the bot with the `-pt` option.

## Supported Exchange marketplaces

At this time, I am testing for PancakeSwap, and plan to add support ant test
for any other Uniswap fork over time.

## Quick start

<TODO>

## Basic Usage

### Command line options

```
usage: gridy.py [-h] [-b BASE] [-q QUOTE] [-a AMOUNT] [-g GRIDS] [-m MIN_PRICE] [-M MAX_PRICE] [-pt]

Grid trading bot for crypto decentralized exchanges

optional arguments:
  -h, --help            show this help message and exit
  -b BASE, --base BASE  Contract address for base currency. e.g. "--base 0x7ad7242A99F21aa543F9650A56D141C57e4F6081"
  -q QUOTE, --quote QUOTE
                        Contract address for quote currency. e.g. "--quote 0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"
  -a AMOUNT, --amount AMOUNT
                        Max amount in quote currency available for the bot to trade. e.g. "--ammount 1200.0"
  -g GRIDS, --grids GRIDS
                        Number of grids to setup (2-200). e.g. "--grids 10"
  -m MIN_PRICE, --min-price MIN_PRICE
                        Minimum price for the grid range. e.g. "--min-price 10.5"
  -M MAX_PRICE, --max-price MAX_PRICE
                        Maximum price for the grid range. e.g. "--min-price 12.3"
  -pt, --paper-trade    Paper trading; Runs the bot with the options provided without performing any actual trades

```

### Telegram RPC commands

<ToDo>

## For developers

<ToDo>
