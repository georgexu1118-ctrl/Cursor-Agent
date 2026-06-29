"""Command-line interface: research-agent <query>."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from research_agent.application.bootstrap import bootstrap
from research_agent.application.research_agent import ResearchAgent, ResearchResult


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="research-agent",
        description=(
            "Answer a research question using the configured LLM and search providers."
        ),
    )
    parser.add_argument("query", help="Research question to answer.")
    parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        metavar="N",
        help="Maximum search results to retrieve (default: 5).",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=1024,
        metavar="N",
        help="Maximum tokens in the LLM response (default: 1024).",
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=None,
        metavar="PATH",
        help="Path to a .env file (default: .env in the working directory).",
    )
    return parser


def _print_result(result: ResearchResult) -> None:
    """Write a formatted research result to stdout."""
    print(f"\nQuery: {result.query}\n")
    print("─" * 60)
    print(result.summary)
    if result.sources:
        print("\nSources:")
        for i, source in enumerate(result.sources, 1):
            print(f"  [{i}] {source.title}")
            print(f"      {source.url}")
    print()


async def _run(
    query: str,
    *,
    max_results: int,
    max_tokens: int,
    env_file: Path | None,
) -> None:
    """Bootstrap the application, run the agent, and print the result."""
    ctx = bootstrap(env_file=env_file)
    agent = ctx.container.resolve(ResearchAgent)
    result = await agent.run(query, max_results=max_results, max_tokens=max_tokens)
    _print_result(result)


def main(argv: list[str] | None = None) -> None:
    """Entry point for the ``research-agent`` command."""
    args = _build_parser().parse_args(argv)
    try:
        asyncio.run(
            _run(
                args.query,
                max_results=args.max_results,
                max_tokens=args.max_tokens,
                env_file=args.env_file,
            )
        )
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
