from setuptools import setup, find_packages

setup(
    name="midi-clip",
    version="0.2",
    packages=find_packages(),
    description="A python package for midi clip.",
    author="kyaryunha",
    author_email="kyaryunha@gmail.com",
    url="https://github.com/kyaryunha/midi-clip",
    install_requires=[
        "mido",
    ],
)
