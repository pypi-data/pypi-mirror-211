from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="cbu_tools",
    version="1.0.0",
    description="A package for working with Clave Bancaria Uniforme (CBU)",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Juan Fernández",
    author_email="jifernandezv97@gmail.com",
    packages=find_packages(exclude=['tests']),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    url="https://github.com/jifernandezv/cbu-tools",
    keywords=["cbu", "clave bancaria uniforme", "argentina", "banco", "validador", "bank", "validator"],
)
