import json
import re
from enum import IntEnum
from typing import Callable, List, NamedTuple

from crypto_crawler._lowlevel import ffi, lib

# snake case
_pattern = re.compile(r'(?<!^)(?=[A-Z])')

def _snake_case(s: str) -> str:
    return _pattern.sub('_', s).lower()

class MarketType(IntEnum):
    '''Market type.'''
    Spot = lib.Spot
    LinearFuture = lib.LinearFuture
    InverseFuture = lib.InverseFuture
    LinearSwap = lib.LinearSwap
    InverseSwap = lib.InverseSwap
    Option = lib.Option
    QuantoFuture = lib.QuantoFuture
    QuantoSwap = lib.QuantoSwap

    def __str__(self):
        return _snake_case(self.name)

class MessageType(IntEnum):
    Trade = lib.Trade
    L2Event = lib.L2Event
    L2Snapshot = lib.L2Snapshot
    L3Event = lib.L3Event
    L3Snapshot = lib.L3Snapshot
    BBO = lib.BBO
    Ticker = lib.Ticker
    Candlestick = lib.Candlestick

    def __str__(self):
        return _snake_case(self.name)

class Message(NamedTuple):
    exchange: str
    market_type: MarketType
    msg_type: MessageType
    symbol: str
    received_at: int
    json: str

    def __str__(self):
        d = dict(self._asdict()) # pylint: disable=no-member
        d["market_type"] = str(d["market_type"])
        d["msg_type"] = str(d["msg_type"])
        return json.dumps(d)

def _convert_msg(msg: object) -> Message:
    '''Convert a C message to a Python message'''
    exchange = ffi.string(msg.exchange).decode("utf-8")
    market_type = MarketType(msg.market_type)
    msg_type = MessageType(msg.msg_type)
    symbol = ffi.string(msg.symbol).decode("utf-8")
    received_at = msg.received_at
    json = ffi.string(msg.json).decode("utf-8")
    return Message(exchange, market_type, msg_type, symbol, received_at, json)

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
    duration: int,
):
    symbols_keepalive = [ffi.new("char[]", symbol.encode("utf-8")) for symbol in symbols]

    lib.crawl_trade(
        ffi.new("char[]", exchange.encode("utf-8")),
        int(market_type),
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
    duration: int,
):
    symbols_keepalive = [ffi.new("char[]", symbol.encode("utf-8")) for symbol in symbols]

    lib.crawl_l2_event(
        ffi.new("char[]", exchange.encode("utf-8")),
        int(market_type),
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
    duration: int,
):
    symbols_keepalive = [ffi.new("char[]", symbol.encode("utf-8")) for symbol in symbols]

    lib.crawl_l2_snapshot(
        ffi.new("char[]", exchange.encode("utf-8")),
        int(market_type),
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
    duration: int,
):
    symbols_keepalive = [ffi.new("char[]", symbol.encode("utf-8")) for symbol in symbols]

    lib.crawl_l3_event(
        ffi.new("char[]", exchange.encode("utf-8")),
        int(market_type),
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
    duration: int,
):
    symbols_keepalive = [ffi.new("char[]", symbol.encode("utf-8")) for symbol in symbols]

    lib.crawl_l3_snapshot(
        ffi.new("char[]", exchange.encode("utf-8")),
        int(market_type),
        ffi.new("char *[]", symbols_keepalive),
        len(symbols),
        _wrap_on_msg(on_msg),
        interval,
        duration,
    )
