"""Domain entities and value objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class MessageRole(StrEnum):
    """Role of a participant in a conversation."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True)
class Message:
    """An immutable chat message with a role and text content.

    Attributes:
        role: Who authored the message.
        content: Text body of the message.
    """

    role: MessageRole
    content: str


@dataclass(frozen=True)
class SearchResult:
    """An immutable search result returned by a search provider.

    Attributes:
        url: Canonical URL of the result.
        title: Page or document title.
        snippet: Short excerpt or summary of the content.
        score: Relevance score in [0, 1]; 0.0 when not provided.
    """

    url: str
    title: str
    snippet: str
    score: float = field(default=0.0)
