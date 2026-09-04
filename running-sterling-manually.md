# Running Sterling Whenever You Want

Sterling runs on its own each weekday morning per the scheduled task. But you can also run it, refresh its data, or ask it questions any time. This guide covers how.

---

## Before You Start — Two Things to Check

1. **LSEG Workspace is open and signed in** (if you set it up). Sterling's live market data comes from it. If it's closed, Sterling still works but uses web data instead (and says so).
2. **The Claude app is open**, with Cowork pointed at this folder.

---

## The Easiest Way — The "Run" Button

You don't have to wait for the scheduled time. Trigger it yourself:

1. In the Claude app, click **Scheduled** in the left sidebar
2. Find **Sterling Daily Research** in the list
3. Click **Run** (or "Run now")

It runs the full daily cycle right then.

**Tip:** if you want the freshest LSEG prices first, refresh the data (below), then click Run.

---

## Other Ways to Use Sterling

### Ask it something directly (in a chat)

Open a Cowork chat and type what you want:
- *"Run today's research cycle."*
- *"What's your take on [company] right now?"*
- *"Read the newest file in the inbox folder and tell me what you think."*
- *"Why did you rate [ticker] high conviction yesterday?"*

### Refresh the market data yourself (in Terminal)

Sometimes you want the latest LSEG prices before running Sterling — for example, mid-day after a big market move.

---

## Using the Python Scripts

Both run from Terminal, inside this folder, with LSEG Workspace open.

**1. Open Terminal.**
Mac: `Cmd + Space`, type `Terminal`, Enter.
Windows: search for PowerShell.

**2. Go to this folder.**
```bash
cd ~/Documents/sterling-workspace
```
(adjust the path to wherever you actually placed it)

**3. Refresh all watchlist prices** — updates the snapshot file Sterling reads each morning:
```bash
python3 fetch_lseg.py
```
Takes a few seconds. Watch the output — it lists the tickers found, any that needed a fallback RIC suffix, and flags any price that moved more than 25% since the last snapshot (worth a second look before trusting it).

**4. Check a specific stock on the spot** — prints to the screen, doesn't save anything:
```bash
python3 get_quote.py MSFT.O NVDA.O
```
Swap in whatever tickers you want.

---

## Ticker Codes (for get_quote.py)

LSEG uses slightly different codes than a normal ticker:

| Type | Add | Example |
|---|---|---|
| US Nasdaq | `.O` | `MSFT.O`, `NVDA.O` |
| US NYSE | `.N` (or try bare) | `CEG.N` |
| Canada (TSX) | `.TO` | `RY.TO`, `BCE.TO` |

If a stock comes back blank, try a different ending, or it may not be in LSEG (Sterling will use web data automatically).

---

## A Typical "I Want Fresh Analysis Now" Flow

1. Make sure LSEG Workspace is open
2. In Terminal: `cd` into the folder, then `python3 fetch_lseg.py`
3. In the Claude app → **Scheduled** → your task → click **Run**

---

## Feeding Sterling an Article or Report

1. Save the file (PDF works well — for a paywalled article, use Print → Save as PDF)
2. Drop it into the **inbox** folder
3. Ask Sterling: *"Read the newest file in the inbox and factor it into your view."*

It also picks up inbox files automatically each morning.

---

## Giving Feedback

Reply to a call with one word: **signal**, **noise**, or **acted-on**. It logs your feedback and calibrates to what you find useful.

---

## Changing How It Works

Just ask, in a chat:
- *"Add [company] to the watchlist."*
- *"Remove [company] from the watchlist."*
- *"From now on, always flag any stock with earnings in the next 7 days."*

Changes get written into the files and persist for future runs.

---

## If Something Looks Off

**Prices seem old:** re-run `python3 fetch_lseg.py` (check LSEG Workspace is open).

**It used web data instead of LSEG:** LSEG Workspace was probably closed when it ran.

**You want to double-check a number:** `python3 get_quote.py TICKER.O` gives the live figure straight from LSEG.
