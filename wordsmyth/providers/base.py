"""Base provider implementation"""
from __future__ import annotations
from typing import Optional
from argparse import ArgumentParser

from requests import Session
from wordsmyth.types import Item


class Provider:
    """Base provider implementation"""

    def __init__(self) -> None:
        self.client = Session()

    def retrieve(
        self, identifier: str, params: Optional[dict[str, str]] = None
    ) -> Optional[Item]:
        """
        Fetch the required data associated with the API you are using.
        Any method is preferred as long as it returns an Item

        `identifier` is the ID of a content which is used in runtime (required)

        `params` is a dictionary of optional parameters for passing auth data
        """
        raise NotImplementedError

    def entrypoint(self) -> Optional[str]:
        return self.retrieve.__doc__

    @property
    def name(self) -> str:
        """Returns the name of the provider for utility purposes"""
        return self.__class__.__name__
