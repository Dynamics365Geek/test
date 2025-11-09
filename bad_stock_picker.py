"""
A very unserious stock selector that reliably does the wrong thing.

This script intentionally picks equities that have been doing terribly
according to some hard-coded, cherry-picked metrics. It proudly ignores
diversification, balance, and common sense.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from textwrap import dedent


@dataclass(frozen=True)
class Stock:
    ticker: str
    company: str
    three_month_return: float  # percentage change
    lawsuits_pending: int
    ceo_quotes: str

    @property
    def misery_index(self) -> float:
        """
        Higher numbers are worse. Perfect for our needs.
        """
        penalties = 0.0

        # Reward (i.e. increase misery) for lawsuits.
        penalties += self.lawsuits_pending * 4.5

        # Penalize (increase misery) if the CEO sounds chaotic.
        if "bankruptcy" in self.ceo_quotes.lower():
            penalties += 12
        if "trust me" in self.ceo_quotes.lower():
            penalties += 7

        # Encourage buying the biggest losers.
        penalties += max(0, -self.three_month_return) * 1.6

        return penalties


# A curated sampler plate of questionable picks.
UNIVERSE: list[Stock] = [
    Stock(
        ticker="HTZZ",
        company="Almost Rental Cars",
        three_month_return=-48.7,
        lawsuits_pending=5,
        ceo_quotes="We're not technically bankrupt; we're innovating Chapter 11.",
    ),
    Stock(
        ticker="FLOP",
        company="Floppy Disks Unlimited",
        three_month_return=-62.4,
        lawsuits_pending=3,
        ceo_quotes="Consumers will come back to physical media. Trust me!",
    ),
    Stock(
        ticker="ICED",
        company="Arctic Home Furnishings",
        three_month_return=-33.1,
        lawsuits_pending=7,
        ceo_quotes="Seasonal demand crashes every year, but this year will be different.",
    ),
    Stock(
        ticker="BURN",
        company="Sunburn Resorts",
        three_month_return=-56.3,
        lawsuits_pending=9,
        ceo_quotes="We consider health-code violations a branding opportunity.",
    ),
    Stock(
        ticker="YOLO",
        company="YOLO Space Tourism",
        three_month_return=-71.5,
        lawsuits_pending=12,
        ceo_quotes="Sure, three capsules exploded, but our next launch is soon!",
    ),
    Stock(
        ticker="MELT",
        company="Glacier Ice Cream",
        three_month_return=-29.2,
        lawsuits_pending=2,
        ceo_quotes="Climate change? Sounds like a distribution advantage to me.",
    ),
    Stock(
        ticker="DRIP",
        company="Luxury Leakproof Roofing",
        three_month_return=-41.8,
        lawsuits_pending=6,
        ceo_quotes="Negative reviews just signal strong customer engagement.",
    ),
]


def pick_spectacularly_bad_stocks(count: int, seed: int | None = None) -> list[Stock]:
    """
    Return the most dubious selections available.

    We sort by "misery index", then stir in randomness weighted toward the bottom
    of the list so that the picks are consistently ill-advised, yet still varied.
    """
    if count <= 0:
        raise ValueError("count must be greater than zero")

    rng = random.Random(seed)
    ranked = sorted(UNIVERSE, key=lambda s: s.misery_index, reverse=True)

    # Weighted random draw: exponentially prefer the worst-ranked entries.
    weights = [1.4 ** idx for idx in range(len(ranked), 0, -1)]
    selections: list[Stock] = []

    while ranked and len(selections) < count:
        choice = rng.choices(ranked, weights=weights[: len(ranked)])[0]
        selections.append(choice)
        idx = ranked.index(choice)
        ranked.pop(idx)
        weights.pop(len(weights) - idx - 1)

    return selections


def format_recommendation(stock: Stock, index: int) -> str:
    emphasis = ["Catastrophic pick", "Terrible idea", "Utterly doomed", "Financial faceplant"]
    tagline = emphasis[index % len(emphasis)]
    return dedent(
        f"""
        {tagline}: {stock.ticker} — {stock.company}
          ▸ 3-month return: {stock.three_month_return:.1f}%
          ▸ Lawsuits pending: {stock.lawsuits_pending}
          ▸ CEO insight: “{stock.ceo_quotes}”
          ▸ Misery index™: {stock.misery_index:.1f}
        """
    ).strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pick stocks no sensible investor would touch."
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=3,
        help="How many questionable recommendations to generate (default: 3)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed so you can relive bad decisions consistently.",
    )
    args = parser.parse_args()

    selections = pick_spectacularly_bad_stocks(args.count, args.seed)

    print("\nBehold, the Bottom-of-the-Barrel Stock Picker™ results:\n")
    for idx, stock in enumerate(selections):
        print(format_recommendation(stock, idx))
        print()

    if len(selections) < args.count:
        print(
            "We ran out of disasters to recommend. Consider this a small mercy.",
        )


if __name__ == "__main__":
    main()
