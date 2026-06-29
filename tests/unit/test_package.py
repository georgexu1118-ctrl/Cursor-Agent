"""Unit tests for package metadata."""

from research_agent import __version__


def test_version_is_semantic() -> None:
    """Package version follows major.minor.patch format."""
    parts = __version__.split(".")
    assert len(parts) == 3, f"Expected 3 version parts, got: {__version__!r}"
    assert all(part.isdigit() for part in parts), (
        f"All version parts must be numeric: {__version__!r}"
    )
