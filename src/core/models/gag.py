"""Gag data model."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Gag:
    """Data model for a 9GAG post."""

    id: str
    title: str
    url: Optional[str] = None
    is_video: Optional[bool] = None

    @property
    def full_url(self) -> str:
        """Get the full URL to the gag."""
        return f"https://9gag.com/gag/{self.id}"
