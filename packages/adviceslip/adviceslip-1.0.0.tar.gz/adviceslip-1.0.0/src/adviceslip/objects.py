from dataclasses import dataclass
from datetime import date
from typing import Iterator, Optional


@dataclass
class Slip:
    """Dataclass containing slip data (ID, advice, optional date)"""

    id: int
    advice: str
    date: Optional[date] = None

    def __str__(self) -> str:
        """Return the slip as a string

        Returns:
            str: The advice from the slip
        """
        return self.advice


@dataclass
class Search:
    """Dataclass containing search results (amount, search query, iterator of slip objects)"""

    total_results: int
    query: str
    slips: Iterator[Slip]

    def __iter__(self) -> Iterator[Slip]:
        """Iterate over the slips from the search object

        Returns:
            Slip: The slip object containing advice, ID and optional date

        Yields:
            Iterator[Slip]: The iterator containing the slip objects
        """
        return self.slips
