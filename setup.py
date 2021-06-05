from setuptools import find_packages, setup
from setuptools.dist import Distribution


def build_native(spec):
    build = spec.add_external_build(
        cmd=['cargo', 'build', '--release'],
        path='./crypto-crawler-ffi'
    )
    spec.add_cffi_module(
        module_path='crypto_crawler._lowlevel',
        dylib=lambda: build.find_dylib('crypto_crawler_ffi', in_path='target/release'),
        header_filename=lambda: build.find_header('crypto_crawler.h', in_path='include'),
        rtld_flags=['NOW', 'NODELETE']
    )

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='crypto_crawler',
    version="0.1.0",
    author="soulmachine",
    description="A rock-solid cryprocurrency crawler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soulmachine/crypto-crawler-py",
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['milksnake'],
    install_requires=['milksnake'],
    milksnake_tasks=[build_native],
    python_requires='>=3.6',
    classifiers = [
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords = ['blockchain', 'cryptocurrency', 'trading'],
)
