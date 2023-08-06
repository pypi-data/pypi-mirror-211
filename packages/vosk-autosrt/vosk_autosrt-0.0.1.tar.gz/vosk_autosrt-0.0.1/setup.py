#!/usr/bin/env python
from __future__ import unicode_literals

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = (
    'vosk_autosrt is a COMMAND LINE UTILLITY for automatic speech recognition and subtitle generation using  '
    'Vosk API. It takes video or audio files as input, convert them to temporary wav files then performs an  '
    'offline voice recognition, generate transcriptions, and optionally translates them to different language'
    'and finally save the resulting subtitles to disk.'
    'It supports 21 input languages but can translate up to 134 languages and can produce subtitles currently'
    'in SRT, VTT, JSON, and RAW format.'
)

setup(
    name="vosk_autosrt",
    version="0.0.1",
    description="a command line utility for automatic speech recognition and subtitle generation",
    long_description = long_description,
    author="Bot Bahlul",
    author_email="bot.bahlul@gmail.com",
    url="https://github.com/botbahlul/vosk_autosrt",
    packages=[str("vosk_autosrt")],
    entry_points={
        "console_scripts": [
            "vosk_autosrt = vosk_autosrt:main",
        ],
    },
    install_requires=[
        "requests>=2.3.0",
        "httpx>=0.13.3",
        "urllib3 >=1.26.0,<3.0",
        "pysrt>=1.0.1",
        "six>=1.11.0",
        "progressbar2>=3.34.3",
    ],
    license=open("LICENSE").read()
)
