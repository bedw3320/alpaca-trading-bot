"""News aggregation via Tavily."""

from __future__ import annotations

from typing import Any

from tavily import TavilyClient

from utils.logging import get_logger

log = get_logger(__name__)


def search_tavily(
    tavily: TavilyClient | None,
    *,
    query: str,
    topic: str = "news",
    days: int = 7,
    max_results: int = 5,
) -> list[dict[str, Any]]:
    """Search news via Tavily."""
    if tavily is None:
        return []

    log.info("Tavily news search: %s", query)
    res = tavily.search(
        query=query,
        topic=topic,
        days=days,
        max_results=max_results,
        search_depth="basic",
    )
    results = res.get("results", []) or []
    return [
        {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "content": r.get("content", "")[:500],
            "score": r.get("score"),
            "source": "tavily",
        }
        for r in results
        if isinstance(r, dict)
    ]


def aggregate_news(
    tavily: TavilyClient | None,
    symbols: list[str],
    *,
    keywords: list[str] | None = None,
    max_results: int = 10,
) -> list[dict[str, Any]]:
    """Aggregate ticker news from Tavily, optionally filtered by keywords."""
    results: list[dict[str, Any]] = []

    for symbol in symbols[:3]:  # limit to avoid rate limits
        query = f"{symbol} stock news"
        if keywords:
            query += " " + " ".join(keywords[:3])
        results.extend(search_tavily(tavily, query=query, max_results=max_results // 2))

    if keywords:
        kw_lower = [k.lower() for k in keywords]
        results = [
            r for r in results
            if any(
                kw in r.get("title", "").lower() or kw in r.get("content", "").lower()
                for kw in kw_lower
            )
        ]

    return results[:max_results]
