"""Includes OneHotEncodingSettings class."""

from dataclasses import dataclass


@dataclass
class OneHotEncodingSettings:
    """Settings for OneHotEncoding service"""
    threshold: float
    max_bin: int
