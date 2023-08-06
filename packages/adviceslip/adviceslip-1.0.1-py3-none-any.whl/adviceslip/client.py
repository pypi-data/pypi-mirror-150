from datetime import date
from types import TracebackType
from typing import Any, ClassVar, Dict, Optional, Type

import requests

from .exceptions import APIError, HTTPException, MessageType, SessionClosed
from .objects import Search, Slip


class ClientBase:

    URL: ClassVar[str] = "https://api.adviceslip.com"

    def __init__(self, *, session: Optional[requests.Session] = None) -> None:
        self._SESSION_OWNED_BY_CLIENT: bool = session is None
        if self._SESSION_OWNED_BY_CLIENT:
            self.session: requests.Session = requests.Session()
            self._closed: bool = False

    def __enter__(self) -> "ClientBase":
        """Context manager entrypoint

        Returns:
            ClientBase: The client instance
        """
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Context manager exit method

        Args:
            exc_type (Optional[Type[BaseException]]): Optional exception type
            exc_value (Optional[BaseException]): Optional exception value
            traceback (Optional[TracebackType]): Optional traceback
        """
        self.close()

    def request(self, endpoint: str) -> Dict[str, Any]:
        """Make a request to the API and return the JSON response as a dict

        Args:
            endpoint (str): The API endpoint to request

        Raises:
            HTTPException: Raised when a HTTP error is encountered
            APIError: Raised when the API returns an error

        Returns:
            Dict[str, Any]: The JSON response as a Python dictionary, which is then parsed into a dataclass (search and slip objects)
        """
        if self._closed:
            raise SessionClosed("Cannot operate on a closed session")
        url: str = f"{self.URL}{endpoint}"
        response: requests.Response = self.session.get(url)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise HTTPException(e.response.text, e.response.status_code) from e
        else:
            j: Dict[str, Any] = response.json()
            if err := j.get("message"):
                raise APIError(err["text"], type=MessageType(err["type"]))
            else:
                return j

    def close(self) -> None:
        """Close the session if it was created by the client"""
        if self._SESSION_OWNED_BY_CLIENT:
            self.session.close()
            self._closed = True


class Client(ClientBase):
    def random(self) -> Slip:
        """Get a random slip

        Returns:
            Slip: The slip object returned, contains the slip ID and advice
        """
        slip: Dict[str, Any] = self.request("/advice")["slip"]
        return Slip(**slip)

    def slip_from_id(self, id: int) -> Slip:
        """Get a slip from a given ID

        Args:
            id (int): The slip ID

        Returns:
            Slip: The slip object returned, contains the slip ID and advice
        """
        slip: Dict[str, Any] = self.request(f"/advice/{id}")["slip"]
        return Slip(**slip)

    def search(self, query: str) -> Search:
        """Search for slips containing a given query

        Args:
            query (str): The search query to use

        Returns:
            Search: A search object containing the amount of results, the query itself and an iterator of slip objects
        """
        search: Dict[str, Any] = self.request(f"/advice/search/{query}")
        return Search(
            total_results=int(search["total_results"]),
            query=search["query"],
            slips=(Slip(id=s["id"], advice=s["advice"], date=date.fromisoformat(s["date"])) for s in search["slips"]),
        )
