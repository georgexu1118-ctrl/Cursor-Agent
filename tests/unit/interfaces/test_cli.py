"""Unit tests for the CLI interface."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from research_agent.application.research_agent import ResearchResult
from research_agent.domain.entities import SearchResult
from research_agent.interfaces.cli import _build_parser, _print_result, _run, main

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_mock_ctx(
    summary: str = "answer", sources: list[SearchResult] | None = None
) -> MagicMock:
    """Return a mock ApplicationContext whose agent returns a fixed ResearchResult."""
    result = ResearchResult(query="q", sources=sources or [], summary=summary)
    mock_agent = MagicMock()
    mock_agent.run = AsyncMock(return_value=result)
    ctx = MagicMock()
    ctx.container.resolve.return_value = mock_agent
    return ctx


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


class TestParser:
    def test_parses_positional_query(self) -> None:
        args = _build_parser().parse_args(["what is Python?"])
        assert args.query == "what is Python?"

    def test_default_max_results_is_5(self) -> None:
        assert _build_parser().parse_args(["q"]).max_results == 5

    def test_default_max_tokens_is_1024(self) -> None:
        assert _build_parser().parse_args(["q"]).max_tokens == 1024

    def test_default_env_file_is_none(self) -> None:
        assert _build_parser().parse_args(["q"]).env_file is None

    def test_custom_max_results(self) -> None:
        args = _build_parser().parse_args(["q", "--max-results", "10"])
        assert args.max_results == 10

    def test_custom_max_tokens(self) -> None:
        args = _build_parser().parse_args(["q", "--max-tokens", "256"])
        assert args.max_tokens == 256

    def test_env_file_parsed_as_path(self) -> None:
        args = _build_parser().parse_args(["q", "--env-file", ".env.test"])
        assert args.env_file == Path(".env.test")

    def test_all_options_together(self) -> None:
        args = _build_parser().parse_args(
            [
                "my query",
                "--max-results",
                "3",
                "--max-tokens",
                "512",
                "--env-file",
                ".env",
            ]
        )
        assert args.query == "my query"
        assert args.max_results == 3
        assert args.max_tokens == 512
        assert args.env_file == Path(".env")


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------


class TestPrintResult:
    def test_prints_summary(self, capsys: pytest.CaptureFixture[str]) -> None:
        _print_result(ResearchResult(query="q", sources=[], summary="The answer."))
        assert "The answer." in capsys.readouterr().out

    def test_prints_query(self, capsys: pytest.CaptureFixture[str]) -> None:
        _print_result(ResearchResult(query="what is Python?", sources=[], summary="s"))
        assert "what is Python?" in capsys.readouterr().out

    def test_no_sources_section_when_empty(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        _print_result(ResearchResult(query="q", sources=[], summary="s"))
        assert "Sources:" not in capsys.readouterr().out

    def test_sources_section_present_when_non_empty(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        source = SearchResult(url="https://example.com", title="Example", snippet="s")
        _print_result(ResearchResult(query="q", sources=[source], summary="s"))
        out = capsys.readouterr().out
        assert "Sources:" in out

    def test_source_url_in_output(self, capsys: pytest.CaptureFixture[str]) -> None:
        source = SearchResult(url="https://example.com", title="Ex", snippet="s")
        _print_result(ResearchResult(query="q", sources=[source], summary="s"))
        assert "https://example.com" in capsys.readouterr().out

    def test_source_title_in_output(self, capsys: pytest.CaptureFixture[str]) -> None:
        source = SearchResult(url="https://x.com", title="My Title", snippet="s")
        _print_result(ResearchResult(query="q", sources=[source], summary="s"))
        assert "My Title" in capsys.readouterr().out

    def test_multiple_sources_numbered(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        sources = [
            SearchResult(url="https://a.com", title="A", snippet="s"),
            SearchResult(url="https://b.com", title="B", snippet="s"),
        ]
        _print_result(ResearchResult(query="q", sources=sources, summary="s"))
        out = capsys.readouterr().out
        assert "[1]" in out
        assert "[2]" in out


# ---------------------------------------------------------------------------
# _run coroutine
# ---------------------------------------------------------------------------


class TestRun:
    async def test_calls_agent_run_with_query_and_options(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ctx = _make_mock_ctx()
        monkeypatch.setattr("research_agent.interfaces.cli.bootstrap", lambda **_: ctx)

        await _run("my query", max_results=3, max_tokens=512, env_file=None)

        ctx.container.resolve.return_value.run.assert_awaited_once_with(
            "my query", max_results=3, max_tokens=512
        )

    async def test_prints_agent_summary(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        ctx = _make_mock_ctx(summary="LLM answer here.")
        monkeypatch.setattr("research_agent.interfaces.cli.bootstrap", lambda **_: ctx)

        await _run("q", max_results=5, max_tokens=1024, env_file=None)

        assert "LLM answer here." in capsys.readouterr().out

    async def test_passes_env_file_to_bootstrap(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        received: list[Path | None] = []

        def _capturing_bootstrap(**kwargs: object) -> MagicMock:
            received.append(kwargs.get("env_file"))  # type: ignore[arg-type]
            return _make_mock_ctx()

        monkeypatch.setattr(
            "research_agent.interfaces.cli.bootstrap", _capturing_bootstrap
        )
        env = Path(".env.custom")
        await _run("q", max_results=5, max_tokens=1024, env_file=env)

        assert received == [env]

    async def test_passes_none_env_file_by_default(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        received: list[Path | None] = []

        def _capturing_bootstrap(**kwargs: object) -> MagicMock:
            received.append(kwargs.get("env_file"))  # type: ignore[arg-type]
            return _make_mock_ctx()

        monkeypatch.setattr(
            "research_agent.interfaces.cli.bootstrap", _capturing_bootstrap
        )
        await _run("q", max_results=5, max_tokens=1024, env_file=None)

        assert received == [None]


# ---------------------------------------------------------------------------
# main() integration
# ---------------------------------------------------------------------------


class TestMain:
    def test_success_prints_summary(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        ctx = _make_mock_ctx(summary="great result")
        monkeypatch.setattr("research_agent.interfaces.cli.bootstrap", lambda **_: ctx)

        main(["hello world"])

        assert "great result" in capsys.readouterr().out

    def test_success_does_not_exit(self, monkeypatch: pytest.MonkeyPatch) -> None:
        ctx = _make_mock_ctx()
        monkeypatch.setattr("research_agent.interfaces.cli.bootstrap", lambda **_: ctx)

        main(["q"])  # must not raise SystemExit

    def test_exception_exits_with_code_1(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        def _bad(**_: object) -> None:
            raise RuntimeError("boom")

        monkeypatch.setattr("research_agent.interfaces.cli.bootstrap", _bad)

        with pytest.raises(SystemExit) as exc_info:
            main(["q"])

        assert exc_info.value.code == 1

    def test_exception_message_written_to_stderr(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        def _bad(**_: object) -> None:
            raise ValueError("bad config value")

        monkeypatch.setattr("research_agent.interfaces.cli.bootstrap", _bad)

        with pytest.raises(SystemExit):
            main(["q"])

        assert "bad config value" in capsys.readouterr().err

    def test_forwards_max_results_to_agent(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ctx = _make_mock_ctx()
        monkeypatch.setattr("research_agent.interfaces.cli.bootstrap", lambda **_: ctx)

        main(["q", "--max-results", "7"])

        ctx.container.resolve.return_value.run.assert_awaited_once_with(
            "q", max_results=7, max_tokens=1024
        )

    def test_forwards_max_tokens_to_agent(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ctx = _make_mock_ctx()
        monkeypatch.setattr("research_agent.interfaces.cli.bootstrap", lambda **_: ctx)

        main(["q", "--max-tokens", "256"])

        ctx.container.resolve.return_value.run.assert_awaited_once_with(
            "q", max_results=5, max_tokens=256
        )
