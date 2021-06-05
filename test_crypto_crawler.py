#!/usr/bin/env python3

from crypto_crawler import (MarketType, crawl_l2_event, crawl_trade)


def test_crawl_trade():
    crawl_trade("binance", MarketType.Spot, ["BTCUSDT", "ETHUSDT"], lambda msg: print(msg), 1)

def test_crawl_l2_event():
    crawl_l2_event("binance", MarketType.Spot, ["BTCUSDT", "ETHUSDT"], lambda msg: print(msg), 1)
