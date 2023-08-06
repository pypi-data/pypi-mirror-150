import requests
from furl import furl
from furl.furl import furl as Url
from requests import Response
from testlodge._types import Identifier


class Client:
    """Represents a client accessing the TestLodge API."""

    def __init__(self, email: str, api_key: str, account_id: Identifier):

        self.email: str = email
        self.api_key: str = api_key
        self.account_id: Identifier = account_id

        self.history: list[Response] = []

    @property
    def base_url(self) -> Url:

        return furl(f'https://api.testlodge.com/v1/account/{self.account_id}')

    def _request(self, method: str, url: str, *args, **kwargs) -> Response:
        """Wrap requests.request to add handlers for response,
        logging, etc."""

        response = requests.request(
            method=method,
            url=url,
            auth=(self.email, self.api_key),
            *args,  # type: ignore
            **kwargs,  # type: ignore
        )

        self.history.append(response)

        return response
