"""Unit tests for package metadata."""

from research_agent import __version__


def test_version_is_semantic() -> None:
    """Package version follows major.minor.patch format."""
    parts = __version__.split(".")
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)
