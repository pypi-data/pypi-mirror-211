"""**serp-onpremise-python**

A Python package for interacting with the SERP On-premise API
"""
from .clients import AsyncClient, Client

__version__: str = "0.1.1"

__all__ = ["__version__", "Client", "AsyncClient"]
