import functools

from furl import Path as UrlPath
from furl.furl import furl as Url
from requests.models import Response
from testlodge._types import Identifier
from testlodge.api.base import BaseAPI
from testlodge.models.suite_section import SuiteSectionListJSON


def client_required(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):

        if self.client is None:
            raise AttributeError("Missing client.")

        return method(self, *args, **kwargs)

    return wrapper


class SuiteSectionAPI(BaseAPI):
    """API for suite sections.


    Endpoints
    ---------
    * List
    * Show
    * Create
    * Update
    * Delete
    """

    name: str = 'suite_section'

    @client_required
    def _list(
        self, project_id: Identifier, suite_id: Identifier, page: int = 1
    ) -> SuiteSectionListJSON:
        """Paginated list of all suite sections inside a suite.

        Parameters
        ----------
        project_id: Identifier
            The ID of the project.
        suite_id: Identifier
            The ID of the suite.
        page: int, default=1
            Default: 1
            The number of the page to return.
        """

        method = 'GET'
        url: Url = self.client.base_url / UrlPath(
            f'/projects/{project_id}/suites/{suite_id}/suite_sections.json'
        )
        if page != 1:
            params = {'page': page}
        else:
            params = {}

        response: Response = self.client._request(
            method=method, url=url, params=params
        )
        data: SuiteSectionListJSON = response.json()

        return data
