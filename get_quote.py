#!/usr/bin/env python3
"""
get_quote.py — Fetch a quick fundamentals snapshot from LSEG Data (Refinitiv)
for one or more tickers.

Usage:
    python get_quote.py [TICKER ...]

If no tickers are given, defaults to GOOGL.O.
"""

import sys
import warnings

warnings.filterwarnings("ignore")

import lseg.data as ld


FIELDS = [
    "TR.PriceClose",
    "TR.PE",
    "TR.CompanyMarketCap",
    "TR.Revenue",
    "TR.EPSActValue",
]


def main():
    tickers = sys.argv[1:] if len(sys.argv) > 1 else ["GOOGL.O"]

    try:
        ld.open_session()

        df = ld.get_data(universe=tickers, fields=FIELDS)

        print(df.to_string(index=False))

        ld.close_session()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
