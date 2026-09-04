# Sterling — How It Works

An AI investment research analyst that runs automatically each weekday morning and delivers conviction-weighted calls on your portfolio and watchlist.

---

## What It Does

Sterling is an **active research analyst**, not a news feed. Each run it:

1. Reads your portfolio, watchlist, and past calls
2. Pulls live prices and fundamentals from LSEG (if set up)
3. Searches for material news affecting those names
4. Runs anything promising through an 8-step analysis process
5. Makes a real call — **Buy / Accumulate / Hold / Trim / Avoid** — with a conviction level
6. Logs every call so its track record can be scored later

It commits to a view rather than handing back a menu of considerations. You execute; it tells you what it would do and why.

---

## When It Runs

Weekdays, at whatever time was set during scheduled-task creation. If LSEG is set up, market data refreshes shortly before that.

**Two requirements:**
- The computer must be **awake** (screen off is fine, sleep is not)
- **LSEG Workspace must be running**, if you're using it

If either is missing, the run still happens but falls back to web-sourced figures, clearly flagged.

---

## What Every Call Includes

| Element | What it means |
|---|---|
| **Call** | Buy / Accumulate / Hold / Trim / Avoid |
| **Conviction** | High / Medium / Low, and why that level |
| **Variant view** | What Sterling thinks the market has wrong |
| **Bull + bear case** | Both sides, with the bear case steelmanned |
| **Priced-in check** | Whether the good news is already in the price |
| **Falsifier** | The specific event that would flip the call |
| **Account fit** | Which account it belongs in, with the tax lens |
| **Concentration check** | Whether this adds to an already-large exposure |

Each run also produces a broader **scan list** — 10+ names looked at, one line each — before narrowing to the 2-4 best that get a full workup. Quality over quantity; a quiet day with one strong call, or none, is fine.

---

## Where Its Numbers Come From

**LSEG Workspace (primary, if set up)** — institutional prices, P/E, market cap, revenue, EPS. Auto-resolves tickers to the right format.

**Web search (fallback)** — for news, and for any figure LSEG doesn't return. Always flagged as web-sourced.

**Premium subscriptions** (paywalled news) — block AI access. Save the article/PDF and drop it in the `inbox/` folder instead.

---

## The Files

| File | Purpose |
|---|---|
| `SOUL.md` | Who Sterling is — mandate and hard boundaries |
| `ANALYSIS.md` | The research method used on every idea |
| `MONITORING.md` | The operating philosophy for the daily cycle |
| `DAILY-TASK.md` | Exactly what happens on each scheduled run |
| `MEMORY.md` | Portfolio snapshot — the source of truth for balances |
| `state/watchlist.md` | Names being tracked, and the hunting themes |
| `state/theses.md` | Why each held position is held |
| `state/decision-log.md` | Every call ever made — the track record |
| `state/constraints.md` | Tax and account rules |
| `state/lseg-snapshot.md` | Auto-generated market data (if LSEG is set up) |

---

## How to Use It

**Read the output.** It appears in Cowork under the scheduled task, or trigger it anytime with the Run button.

**Ask follow-ups.** "Why only medium conviction?" "What would change your mind?"

**Request a deep dive.** Ask about any company; it applies the same process on demand.

**Change how it behaves.** Ask it to edit the relevant file — changes written to files persist; things said only in chat don't.

See `running-sterling-manually.md` for the full walkthrough of triggering runs, refreshing data, and giving feedback.

---

## What It Will Never Do

- **Trade, transfer, or move money.** Research and recommendations only — humans execute.
- **Share financial data** outside the private session.
- **Contact advisors, banks, or brokers** on your behalf.
- **State a number it can't source.** Estimates and web-sourced figures are flagged explicitly.
- **Act as a licensed advisor.** Binding tax, legal, or filing decisions go to a qualified professional.

---

## Cost

Runs draw from your Claude Max plan allocation — no per-use charges, no separate API billing.
