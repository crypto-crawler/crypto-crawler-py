# crypto-crawler

A rock-solid cryprocurrency crawler.

This is Python wrapper on top of the [crypto-crawler](https://github.com/soulmachine/crypto-crawler-rs/tree/main/crypto-crawler) crate.

## Quickstart

Install,

```bash
pip3 install crypto-crawler
```

```python
from crypto_crawler import MarketType, crawl_trade

crawl_trade("binance", MarketType.spot, ["BTCUSDT", "ETHUSDT"], lambda msg: print(msg))
```

## How to build

On Mac OS X,

```bash
conda install --file requirements-dev.txt

rm -rf build crypto-crawler-ffi/target
python3 setup.py bdist_wheel

# Need to create a ~/.pypirc file first
twine upload --repository testpypi dist/*
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps crypto-crawler

twine upload dist/*
```

For Linux,

```bash
docker run -it --rm -v $(pwd):/project soulmachine/rust:manylinux2014 bash

/opt/python/cp36-cp36m/bin/pip3 install -r requirements-dev.txt
rm -rf build crypto-crawler-ffi/target
/opt/python/cp36-cp36m/bin/python3 setup.py bdist_wheel
auditwheel repair dist/*linux*.whl --plat manylinux2014_x86_64
/opt/python/cp36-cp36m/bin/twine upload --repository testpypi wheelhouse/*
```

## Test

```bash
python3 setup.py develop
pytest -s
```
