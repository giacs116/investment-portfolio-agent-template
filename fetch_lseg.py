#!/usr/bin/env python3
"""
fetch_lseg.py — Pull a fundamentals snapshot from LSEG Data (Refinitiv) for
every ticker/RIC mentioned in state/watchlist.md, and write the results as a
markdown table to state/lseg-snapshot.md.

Ticker extraction is heuristic (regex over watchlist.md), tuned to the
"**TICKER (Company Name)**" convention used throughout that file, plus
explicit RIC-style suffixes (e.g. FFH.TO, GOOGL.O, VICR.OQ). Free-text
watchlists will always produce some noise or gaps — spot-check the extracted
ticker list printed to stdout (and in the snapshot header) before relying on
it, and add tickers manually to watchlist.md in the "**TICKER (Name)**"
format if a name isn't being picked up.

Tickers that collapse to the same base symbol (e.g. SKHY and SKHY.US) are
de-duplicated before fetching, preferring whichever variant already carries
a RIC-style suffix.

Any ticker without an existing RIC suffix that comes back missing, or with a
row where every requested field is NA (LSEG returns these as pd.NA, not
plain float NaN — checked via pandas .isna(), which handles both), is
retried in turn as TICKER.O, TICKER.OQ, then TICKER.N. That order matches
confirmed live behavior: MSFT.O, META.O, and CEG.O resolve on the first
fallback, while MU.OQ and VICR.OQ need the second. Whichever variant
actually returns data is used, and the resolved RIC is shown alongside the
originally queried symbol in the output table. A debug line is printed for
every ticker flagged as empty and for the outcome of each fallback attempt.

Usage:
    python3 fetch_lseg.py
"""

import os
import re
import sys
import warnings
from datetime import datetime, timezone

warnings.filterwarnings("ignore")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WATCHLIST_PATH = os.path.join(SCRIPT_DIR, "state", "watchlist.md")
SNAPSHOT_PATH = os.path.join(SCRIPT_DIR, "state", "lseg-snapshot.md")

FIELDS = [
    "TR.PriceClose",
    "TR.PE",
    "TR.CompanyMarketCap",
    "TR.Revenue",
    "TR.EPSActValue",
]

# Fallback RIC suffixes tried, in order, for a bare ticker that returns a
# missing or all-NA row on the first attempt. Confirmed order: .O covers
# most Nasdaq names (MSFT, META, CEG), .OQ covers a few that .O misses
# (MU, VICR), .N is the NYSE fallback.
FALLBACK_SUFFIXES = (".O", ".OQ", ".N")

# Common all-caps words/acronyms that show up in watchlist.md prose (used for
# emphasis, or as finance/account jargon) but are not tickers — filtered out
# of the extracted candidate list.
STOPWORDS = {
    "AI", "US", "UK", "EU", "IPO", "ADR", "ADRS", "HBM", "SCA", "SCAS",
    "ROI", "ROIC", "ROE", "EPS", "TTM", "ATH", "CEO", "IR", "NI", "FCF",
    "GAAP", "CAD", "USD", "JPY", "KRW", "ETF", "LLC", "JV", "WACC", "NPV",
    "PPA", "PPAS", "HVAC", "SMR", "SMRS", "TSX", "NASDAQ", "NYSE", "OTCQB",
    "FMP", "PE", "MA", "SOX", "SMH", "DJIA", "FY", "H2", "CPA", "RRSP",
    "TFSA", "RESP", "HISA", "BOC", "GDP", "NFP", "CHIPS", "WFE", "DRAM",
    "LPDDR", "CXL", "ASIC", "ASICS", "XPU", "XPUS", "OEM", "ESG", "KPI",
    "ISO", "THE", "AND", "FOR", "NOT", "ARE", "WAS", "ALL", "NEW", "ONE",
    "TWO", "WHO", "HOW", "WHY", "ADD", "LOW", "HIGH", "HOLD", "BUY", "SELL",
    "WAIT", "STOP", "DEEP", "LIVE", "KEY", "ACTIVE", "ELEVATED", "MACRO",
    "CRITICAL", "THESIS", "NOTE", "WATCH", "UPGRADE", "UPGRADED",
    "DOWNGRADE", "DOWNGRADED", "MAINTAIN", "PASS", "AVOID", "CONFIRMED",
    "STRENGTHENED", "REDUCED", "INTACT", "YOY", "QOQ", "AM", "PM", "TBD",
    "TSXV", "OTC", "SBD", "TSMC", "OK", "NO", "YES",
}

# High-confidence: token immediately followed by a known RIC exchange suffix
RIC_RE = re.compile(r"\b([A-Z]{1,6}(?:-[A-Z])?)\.(TO|O|OQ|N|K|L|PA|DE|HM|US|OA)\b")

# Medium-confidence: bold ticker immediately followed by "(Company Name)",
# matching the "**TICKER (Company)**" convention used throughout watchlist.md
BOLD_RE = re.compile(r"\*\*([A-Z]{1,6}(?:[.\-][A-Z0-9]{1,3})?)\s*\(")


def extract_tickers(text):
    found = set()

    for m in RIC_RE.finditer(text):
        found.add(f"{m.group(1)}.{m.group(2)}")

    for m in BOLD_RE.finditer(text):
        candidate = m.group(1)
        base = candidate.split(".")[0].split("-")[0]
        if base in STOPWORDS:
            continue
        found.add(candidate)

    return sorted(found)


def dedupe_tickers(tickers):
    """Collapse tickers that share a base symbol (e.g. SKHY / SKHY.US),
    preferring whichever variant already carries a RIC-style suffix."""
    by_base = {}
    for t in tickers:
        base = t.split(".")[0]
        existing = by_base.get(base)
        if existing is None or ("." in t and "." not in existing):
            by_base[base] = t
    return sorted(by_base.values())


def write_unavailable(reason, tickers, timestamp):
    with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
        f.write(f"# LSEG Snapshot — {timestamp}\n\n")
        f.write(f"LSEG unavailable as of {timestamp}: {reason}\n\n")
        if tickers:
            f.write(f"Tickers that would have been queried ({len(tickers)}): "
                    f"{', '.join(tickers)}\n")


def _is_nan(v):
    # pandas returns pd.NA (nullable dtypes), np.nan, or None depending on
    # column dtype — pd.isna() is the only check that reliably covers all
    # three. A plain `isinstance(v, float) and v != v` misses pd.NA, which
    # is what LSEG actually returns for missing fields.
    import pandas as pd
    return bool(pd.isna(v))


def _row_is_empty(row, value_cols):
    import pandas as pd
    return bool(pd.Series([row[c] for c in value_cols]).isna().all())


def fetch_with_fallback(ld, tickers, fields):
    """
    Fetch `fields` for `tickers`. Any ticker with no existing RIC suffix
    that comes back missing, or with a row where every field is NA, is
    retried through FALLBACK_SUFFIXES in order — whichever variant returns
    a non-empty row is kept.

    Returns (rows, resolved, instrument_col, value_cols) where `rows` maps
    each original ticker to its final data row (a pandas Series, or None if
    nothing was ever returned for it), and `resolved` maps each original
    ticker to the RIC that actually produced that row (identical to the
    original ticker unless a fallback suffix resolved it).
    """
    import pandas as pd

    df = ld.get_data(universe=tickers, fields=fields)

    instrument_col = "Instrument" if "Instrument" in df.columns else df.columns[0]
    value_cols = [c for c in df.columns if c != instrument_col]

    # Vectorized empty-row detection, per the actual return shape (pd.NA-
    # aware) rather than a manual per-value check.
    empty_mask = df[value_cols].isna().all(axis=1)
    empty_instruments = set(df.loc[empty_mask, instrument_col])

    rows = {}
    for _, row in df.iterrows():
        rows[row[instrument_col]] = row

    resolved = {t: t for t in tickers}

    candidates_to_retry = [
        t for t in tickers
        if "." not in t and (t not in rows or t in empty_instruments)
    ]

    if candidates_to_retry:
        print(f"[fetch_lseg] Empty/missing rows detected for "
              f"{len(candidates_to_retry)} ticker(s), retrying with fallback "
              f"suffixes {FALLBACK_SUFFIXES}: {', '.join(candidates_to_retry)}")
    else:
        print("[fetch_lseg] No empty rows detected on first fetch — no fallback needed.")

    for ticker in candidates_to_retry:
        for suffix in FALLBACK_SUFFIXES:
            candidate = f"{ticker}{suffix}"
            try:
                retry_df = ld.get_data(universe=[candidate], fields=fields)
            except Exception as e:
                print(f"[fetch_lseg]   {candidate}: request failed ({type(e).__name__}: {e})")
                continue
            if retry_df.empty:
                print(f"[fetch_lseg]   {candidate}: no rows returned")
                continue
            retry_row = retry_df.iloc[0]
            if _row_is_empty(retry_row, value_cols):
                print(f"[fetch_lseg]   {candidate}: row returned but still all-NA")
                continue
            rows[ticker] = retry_row
            resolved[ticker] = candidate
            print(f"[fetch_lseg]   {ticker} -> resolved via {candidate}")
            break
        else:
            print(f"[fetch_lseg]   {ticker}: no fallback suffix returned data")

    return rows, resolved, instrument_col, value_cols


def _load_previous_prices(snapshot_path, price_col="TR.PriceClose"):
    """Parse the existing snapshot (if any) into {ticker: last_known_price}
    so a new fetch can be sanity-checked against it. Returns {} if no
    prior snapshot exists or it can't be parsed — this is a best-effort
    guard, not a hard dependency."""
    prices = {}
    if not os.path.exists(snapshot_path):
        return prices
    try:
        with open(snapshot_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        header_idx = None
        for i, line in enumerate(lines):
            if line.strip().startswith("| Queried"):
                header_idx = i
                break
        if header_idx is None:
            return prices
        headers = [h.strip() for h in lines[header_idx].strip().strip("|").split("|")]
        if price_col not in headers:
            return prices
        price_idx = headers.index(price_col)
        for line in lines[header_idx + 2:]:
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) <= price_idx:
                continue
            ticker, raw_price = cells[0], cells[price_idx]
            try:
                prices[ticker] = float(raw_price)
            except (ValueError, TypeError):
                continue
    except Exception:
        return {}
    return prices


PRICE_SANITY_THRESHOLD = 0.25  # flag if a fetched price moves >25% vs. last snapshot


def _flag_suspicious_moves(rows, resolved, value_cols, previous_prices, price_col="TR.PriceClose"):
    """Compare each newly fetched price against the last snapshot's price
    for the same ticker. A move beyond PRICE_SANITY_THRESHOLD in a single
    refresh cycle is more likely a data glitch (bad tick, stale/duplicate
    RIC, corporate action not yet reflected) than a real move, and should
    be flagged for a human to glance at rather than fed silently into a
    high-conviction call. Returns a dict of {ticker: (old, new, pct_change)}
    for anything that trips the threshold."""
    if price_col not in value_cols:
        return {}
    flagged = {}
    for ticker, row in rows.items():
        if row is None or ticker not in previous_prices:
            continue
        new_val = row.get(price_col)
        if new_val is None or _is_nan(new_val):
            continue
        try:
            new_price = float(new_val)
        except (ValueError, TypeError):
            continue
        old_price = previous_prices[ticker]
        if old_price == 0:
            continue
        pct_change = abs(new_price - old_price) / old_price
        if pct_change > PRICE_SANITY_THRESHOLD:
            flagged[ticker] = (old_price, new_price, pct_change)
    return flagged


def main():
    if not os.path.exists(WATCHLIST_PATH):
        print(f"Error: watchlist not found at {WATCHLIST_PATH}")
        sys.exit(1)

    with open(WATCHLIST_PATH, "r", encoding="utf-8") as f:
        watchlist_text = f.read()

    raw_tickers = extract_tickers(watchlist_text)
    tickers = dedupe_tickers(raw_tickers)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    print(f"Extracted {len(raw_tickers)} raw ticker(s)/RIC(s), "
          f"{len(tickers)} after de-duplication:")
    print(", ".join(tickers) if tickers else "(none found)")

    if not tickers:
        write_unavailable("no tickers/RICs could be extracted from state/watchlist.md",
                           tickers, timestamp)
        return

    try:
        import lseg.data as ld

        previous_prices = _load_previous_prices(SNAPSHOT_PATH)

        ld.open_session()
        rows, resolved, instrument_col, value_cols = fetch_with_fallback(ld, tickers, FIELDS)
        ld.close_session()

        suspicious = _flag_suspicious_moves(rows, resolved, value_cols, previous_prices)
        if suspicious:
            print(f"[fetch_lseg] WARNING: {len(suspicious)} ticker(s) moved more than "
                  f"{int(PRICE_SANITY_THRESHOLD*100)}% since the last snapshot — "
                  f"flagged in the output for review, not treated as an error:")
            for t, (old, new, pct) in suspicious.items():
                print(f"[fetch_lseg]   {t}: {old:.2f} -> {new:.2f} ({pct*100:.1f}% move)")

        with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
            f.write(f"# LSEG Snapshot — {timestamp}\n\n")
            f.write(f"Tickers extracted from state/watchlist.md ({len(tickers)} after "
                    f"de-duplication): {', '.join(tickers)}\n\n")

            if suspicious:
                f.write("⚠️ **Large price moves since last snapshot — verify before treating "
                        "as a real signal, this may be a data glitch rather than an actual "
                        "move:**\n")
                for t, (old, new, pct) in suspicious.items():
                    f.write(f"- {t}: {old:.2f} → {new:.2f} ({pct*100:.1f}% change)\n")
                f.write("\n")

            headers = ["Queried", "Resolved RIC"] + value_cols
            f.write("| " + " | ".join(headers) + " |\n")
            f.write("| " + " | ".join("---" for _ in headers) + " |\n")

            for ticker in tickers:
                row = rows.get(ticker)
                if row is None:
                    cells = [ticker, "(no data)"] + ["" for _ in value_cols]
                else:
                    cells = [ticker, resolved[ticker]] + [
                        "" if _is_nan(v) else str(v)
                        for v in (row[c] for c in value_cols)
                    ]
                f.write("| " + " | ".join(cells) + " |\n")

        print(f"Wrote LSEG snapshot for {len(tickers)} tickers to {SNAPSHOT_PATH}")

    except Exception as e:
        write_unavailable(f"{type(e).__name__}: {e}", tickers, timestamp)
        print(f"LSEG unavailable: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
