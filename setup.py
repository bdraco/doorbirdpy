"""DoorBirdPy setup script."""
from setuptools import setup

setup(
    name="DoorBirdPy",
    version="3.0.0",
    author="Andy Castille",
    author_email="andy@robiotic.net",
    packages=["doorbirdpy"],
    install_requires=["aiohttp"],
    url="https://gitlab.com/klikini/doorbirdpy",
    download_url="https://gitlab.com/klikini/doorbirdpy/-/archive/master/doorbirdpy-master.zip",
    license="MIT",
    description="Python wrapper for the DoorBird LAN API v0.21",
    platforms="Cross Platform",
)
