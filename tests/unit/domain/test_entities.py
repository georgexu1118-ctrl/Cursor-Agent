"""Unit tests for domain entities."""

import pytest

from research_agent.domain.entities import Message, MessageRole, SearchResult


class TestMessageRole:
    def test_string_values(self) -> None:
        assert MessageRole.SYSTEM == "system"
        assert MessageRole.USER == "user"
        assert MessageRole.ASSISTANT == "assistant"

    def test_is_str(self) -> None:
        assert isinstance(MessageRole.USER, str)


class TestMessage:
    def test_creation(self) -> None:
        msg = Message(role=MessageRole.USER, content="hello")
        assert msg.role == MessageRole.USER
        assert msg.content == "hello"

    def test_equality(self) -> None:
        a = Message(role=MessageRole.USER, content="hello")
        b = Message(role=MessageRole.USER, content="hello")
        assert a == b

    def test_inequality_different_role(self) -> None:
        a = Message(role=MessageRole.USER, content="hi")
        b = Message(role=MessageRole.ASSISTANT, content="hi")
        assert a != b

    def test_inequality_different_content(self) -> None:
        a = Message(role=MessageRole.USER, content="hi")
        b = Message(role=MessageRole.USER, content="bye")
        assert a != b

    def test_immutable(self) -> None:
        msg = Message(role=MessageRole.USER, content="hello")
        with pytest.raises(AttributeError):
            msg.content = "changed"  # type: ignore[misc]

    def test_hashable(self) -> None:
        msg = Message(role=MessageRole.USER, content="hello")
        assert hash(msg) is not None
        assert {msg}  # can be placed in a set


class TestSearchResult:
    def test_creation(self) -> None:
        result = SearchResult(
            url="https://example.com",
            title="Example",
            snippet="An example page.",
        )
        assert result.url == "https://example.com"
        assert result.title == "Example"
        assert result.snippet == "An example page."
        assert result.score == 0.0

    def test_custom_score(self) -> None:
        result = SearchResult(
            url="https://example.com",
            title="Ex",
            snippet="...",
            score=0.95,
        )
        assert result.score == 0.95

    def test_equality(self) -> None:
        a = SearchResult(url="https://x.com", title="X", snippet="s", score=0.5)
        b = SearchResult(url="https://x.com", title="X", snippet="s", score=0.5)
        assert a == b

    def test_immutable(self) -> None:
        result = SearchResult(url="https://x.com", title="X", snippet="s")
        with pytest.raises(AttributeError):
            result.url = "https://other.com"  # type: ignore[misc]

    def test_hashable(self) -> None:
        result = SearchResult(url="https://x.com", title="X", snippet="s")
        assert hash(result) is not None
        assert {result}
