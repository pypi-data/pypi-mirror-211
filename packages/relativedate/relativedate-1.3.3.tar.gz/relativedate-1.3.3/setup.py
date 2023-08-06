from setuptools import setup
import os

# Carregar o conteúdo do arquivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='relativedate',
    version='1.3.3',
    description='Pacote Python para tabalhar com Datas Relativas',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['relativedate'],
    install_requires=[],
)
