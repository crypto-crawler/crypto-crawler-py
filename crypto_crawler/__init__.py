import json
from enum import IntEnum
from typing import Callable, List, NamedTuple

from crypto_crawler._lowlevel import ffi, lib


class MarketType(IntEnum):
    '''Market type.'''
    spot = lib.Spot
    linear_future = lib.LinearFuture
    inverse_future = lib.InverseFuture
    linear_swap = lib.LinearSwap
    inverse_swap = lib.InverseSwap

    american_option = lib.AmericanOption
    european_option = lib.EuropeanOption

    quanto_future = lib.QuantoFuture
    quanto_swap = lib.QuantoSwap

    move = lib.Move
    bvol = lib.BVOL


class MessageType(IntEnum):
    trade = lib.Trade
    l2_event = lib.L2Event
    l2_snapshot = lib.L2Snapshot
    l3_event = lib.L3Event
    l3_snapshot = lib.L3Snapshot
    bbo = lib.BBO
    ticker = lib.Ticker
    candlestick = lib.Candlestick
    funding_rate = lib.FundingRate


class Message(NamedTuple):
    exchange: str
    market_type: MarketType
    msg_type: MessageType
    received_at: int
    json: str

    def __str__(self):
        d = dict(self._asdict()) # pylint: disable=no-member
        d["market_type"] = d["market_type"].name
        d["msg_type"] = d["msg_type"].name
        return json.dumps(d)

def _convert_msg(msg: object) -> Message:
    '''Convert a C message to a Python message'''
    exchange = ffi.string(msg.exchange).decode("utf-8")
    market_type = MarketType(msg.market_type)
    msg_type = MessageType(msg.msg_type)
    received_at = msg.received_at
    json = ffi.string(msg.json).decode("utf-8")
    return Message(exchange, market_type, msg_type, received_at, json)

def _wrap_on_msg(on_msg: Callable[[Message], None]) -> Callable[[object], None]:
    '''Convert a python callback to C callback.'''
    @ffi.callback("void (struct Message*)")
    def on_msg_ext(msg: object) -> None:
        on_msg(_convert_msg(msg))
    return on_msg_ext

def crawl_trade(
    exchange: str,
    market_type: MarketType,
    symbols: List[str],
    on_msg: Callable[[Message], None],
    duration: int = 0,
):
    symbols_keepalive = [ffi.new("char[]", symbol.encode("utf-8")) for symbol in symbols]

    lib.crawl_trade(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char *[]", symbols_keepalive),
        len(symbols),
        _wrap_on_msg(on_msg),
        duration,
    )

def crawl_l2_event(
    exchange: str,
    market_type: MarketType,
    symbols: List[str],
    on_msg: Callable[[Message], None],
    duration: int = 0,
):
    symbols_keepalive = [ffi.new("char[]", symbol.encode("utf-8")) for symbol in symbols]

    lib.crawl_l2_event(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char *[]", symbols_keepalive),
        len(symbols),
        _wrap_on_msg(on_msg),
        duration,
    )

def crawl_l2_snapshot(
    exchange: str,
    market_type: MarketType,
    symbols: List[str],
    on_msg: Callable[[Message], None],
    interval: int,
    duration: int = 0,
):
    symbols_keepalive = [ffi.new("char[]", symbol.encode("utf-8")) for symbol in symbols]

    lib.crawl_l2_snapshot(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char *[]", symbols_keepalive),
        len(symbols),
        _wrap_on_msg(on_msg),
        interval,
        duration,
    )

def crawl_l3_event(
    exchange: str,
    market_type: MarketType,
    symbols: List[str],
    on_msg: Callable[[Message], None],
    duration: int = 0,
):
    symbols_keepalive = [ffi.new("char[]", symbol.encode("utf-8")) for symbol in symbols]

    lib.crawl_l3_event(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char *[]", symbols_keepalive),
        len(symbols),
        _wrap_on_msg(on_msg),
        duration,
    )

def crawl_l3_snapshot(
    exchange: str,
    market_type: MarketType,
    symbols: List[str],
    on_msg: Callable[[Message], None],
    interval: int,
    duration: int = 0,
):
    symbols_keepalive = [ffi.new("char[]", symbol.encode("utf-8")) for symbol in symbols]

    lib.crawl_l3_snapshot(
        ffi.new("char[]", exchange.encode("utf-8")),
        market_type.value,
        ffi.new("char *[]", symbols_keepalive),
        len(symbols),
        _wrap_on_msg(on_msg),
        interval,
        duration,
    )
