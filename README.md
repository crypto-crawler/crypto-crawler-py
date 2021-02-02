# crypto-crawler

A rock-solid cryprocurrency crawler.

This is Python wrapper on top of the [crypto-crawler](https://github.com/soulmachine/crypto-crawler-rs/tree/main/crypto-crawler) crate.

## How to build

```bash
git submodule foreach git pull
conda install cffi milksnake tox twine -c conda-forge
python3 setup.py build
python3 setup.py develop
python3 setup.py bdist_wheel
twine upload --repository testpypi dist/*
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps crypto-crawler
twine upload dist/*
```

## Test

```bash
python3 setup.py develop
pytest -s
```
