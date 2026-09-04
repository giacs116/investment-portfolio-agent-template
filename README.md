# Sterling
 
An AI investment research analyst that runs on a schedule in Claude Cowork. It reads your portfolio and watchlist, pulls live market data, researches what's moving, and delivers real Buy/Accumulate/Hold/Trim/Avoid calls — each with a stated conviction level, a bull and bear case, and a falsifier that would prove it wrong.
 
It's not a licensed advisor and doesn't move money. It does the research and makes the case; you decide.
 
---
 
## What it does
 
- Runs automatically each weekday morning
- Scans 10+ names for what's worth a look (breadth), then goes deep on the 2-4 that genuinely clear the bar (depth)
- Pulls live prices and fundamentals from LSEG, if you have a Workspace subscription — falls back to web-sourced data (clearly flagged) if not
- Applies a Canadian tax lens to every call — which account it belongs in and why
- Keeps a running decision log so its track record can be reviewed over time
- Learns what you find useful through a simple signal / noise / acted-on feedback loop
- Reads anything you drop in its `inbox/` folder — paywalled articles, PDFs, reports
## Getting started
 
This repo is a template — every file that needs to know about *you* starts blank, with an instruction telling Sterling what to ask. Clone it, connect it to Claude Cowork, and it interviews you before doing anything else.
 
**Start here: [`SETUP.md`](./SETUP.md)** — the full walkthrough, step by step.
 
## What you'll need
 
- A Claude Max plan (Cowork requires it)
- The Claude desktop app
- Git
- (Optional) An LSEG Workspace subscription, for live institutional market data
## Documentation
 
| File | What it covers |
|---|---|
| [`SETUP.md`](./SETUP.md) | Full setup walkthrough, start to finish |
| [`sterling-how-it-works.md`](./sterling-how-it-works.md) | What Sterling does and how a call is structured |
| [`running-sterling-manually.md`](./running-sterling-manually.md) | Triggering runs, refreshing data, feeding it articles |
| [`BACKUP.md`](./BACKUP.md) | Saving your changes to GitHub |
 
## A note on privacy
 
Once set up, this workspace holds real financial information — your portfolio, your goals, every call made on your behalf. Keep your repo **private**. Never commit or share it publicly.
 
## What it will never do
 
- Trade, transfer, or move money
- Share your financial data outside the private session
- Contact an advisor, bank, or broker on your behalf
- State a number it can't source
- Act as a substitute for a licensed CPA, CFP, or lawyer
