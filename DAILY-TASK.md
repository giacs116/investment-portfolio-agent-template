# DAILY-TASK.md — What to Do on Every Scheduled Run

Read this file at the start of every scheduled run, in this order, before doing anything else.

---

## Step 1 — Check onboarding status

Open USER.md and check for `[PLACEHOLDER]` markers.

**If placeholders remain, onboarding was not completed before this task was scheduled.** This should not normally happen — SETUP.md instructs completing onboarding in a manual chat BEFORE creating this scheduled task. Do not attempt to interview anyone here: this is an unattended run, and no one is present to answer questions in real time.

Instead: post one short line —

> "Onboarding is incomplete — please open a manual chat with me to finish setup before the daily research cycle can run."

Then stop. Do not use any search budget, do not attempt research, do not try to guess or fill in missing information.

**If no placeholders remain**, proceed to Step 2.

---

## Step 2 — Run the daily research cycle

1. Read MEMORY.md and state/watchlist.md.
2. Check the `inbox/` folder for any files added since the last run — read and factor them in, citing them as user-provided sources.
3. Read `state/lseg-snapshot.md` for prices, multiples, and fundamentals — cite LSEG with the snapshot timestamp. If the snapshot is missing, stale, or a ticker shows no data, source that figure from the web instead and flag it as web-sourced. **Check the timestamp at the top of the snapshot: if it's more than 24 hours old, say so explicitly at the start of your output** (e.g. "Note: LSEG data is from [date/time], older than expected — the local fetch may not have run") rather than presenting it as current without comment. **If the snapshot flags a large price move (⚠️ section at the top) for a name you're about to use in a call, verify that figure against a second source before relying on it** — a >25% single-cycle move is as likely to be a data glitch as a real one.
4. Search for material news since the last run — both what touches existing holdings/watchlist names, and broader market/world developments and correlations worth hunting in.
5. **If you find a name during this run that's genuinely interesting but doesn't yet clear the ANALYSIS.md bar for a full call**, add it to the "Active watch names" section of state/watchlist.md with a short note on why it's on your radar — this is how the watchlist grows over time from your own research, not just from what the user tells you to track.
6. Produce two sections:
   - **SCAN LIST (breadth):** a ranked list of 10 or more names looked at this run, one line each — ticker, quick read, interesting-or-pass and why.
   - **CALLS (depth):** full workups, per the ANALYSIS.md 8-step process, on only the best 2-4 names that genuinely clear the bar — call, conviction, variant view, bull and bear case, priced-in check, falsifier, and account fit per state/constraints.md. Do not force weak ideas into full calls to hit a number. A quiet day with one strong call, or none, is fine.
7. Use at most 6 searches and 6 page fetches total for the run.
8. Append the Section 2 calls to state/decision-log.md per its logging format — date, item, call, conviction, the price used at the time of the call, and falsifier.
9. Never state a number that isn't sourced.
10. **Roughly once a week** (use your judgment on the date, or check state/decision-log.md for when you last mentioned this), remind the person at the end of your output to back up their files to GitHub — see BACKUP.md. Given the real decisions and financial detail recorded here, don't let this slide for long stretches unprompted.

---

## Notes

- This file is the single source of truth for what a scheduled run does — if MONITORING.md and this file ever conflict, follow this one for the daily-run mechanics, and MONITORING.md for the broader operating philosophy.
- **Onboarding should always be complete before the scheduled task exists** (see SETUP.md Step 3, done as a manual chat, before Step 5 where the scheduled task is created). The Step 1 check above is a safety net for a misconfigured setup, not the normal onboarding path — an unattended scheduled run is the wrong place to conduct a real-time interview.
