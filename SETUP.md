# SETUP.md — Setting Up Sterling on Your Own Computer

This repo is a complete, self-contained package for running Sterling — an AI investment research analyst — in Claude Cowork. Follow these steps in order.

**A note on names:** this guide uses `sterling-workspace` as the folder/repo name throughout as an example. If you named it something else when cloning (Step 1), mentally swap in your actual name everywhere you see `sterling-workspace` below.

---

## What you need before starting

- A **Claude Max** plan (Cowork requires it)
- The **Claude desktop app** installed
- **Git** installed on your computer
- (Optional but recommended) An **LSEG Workspace** subscription, for live institutional market data. Without it, Sterling uses web-sourced data instead — it still works, just less precise.

---

## Step 1 — Get the files onto your computer

Open **Terminal** (Mac) or **PowerShell** (Windows) — this is a program on your computer for typing commands, not a website. Then type the following and press Enter:

```bash
cd ~/Documents
git clone [PLACEHOLDER: REPO URL] [PLACEHOLDER: REPO NAME]
```

Replace `[PLACEHOLDER: REPO URL]` with this repository's actual GitHub URL, and `[PLACEHOLDER: REPO NAME]` with its current name (check the top of the GitHub page — it's the folder name this will create). Throughout the rest of this guide, wherever you see `sterling-workspace`, use that same name instead — it should always match the repo name.

This creates a folder with everything Sterling needs.

---

## Step 2 — Connect Cowork to the folder

1. Open the Claude desktop app
2. Make sure **Cowork** is toggled on (next to Chat, in the input box)
3. Click **"Project or folder"** and select the `sterling-workspace` folder you just created
4. Set the model to **Sonnet**

---

## Step 3 — Start a chat and let onboarding begin

Open a chat and say something like "let's get started." Sterling will notice USER.md is full of `[PLACEHOLDER]` markers and begin the onboarding interview automatically — see `ONBOARDING.md` for what it covers. Answer at your own pace; nothing is required beyond the basics, and financial detail is entirely optional.

At the end, Sterling will show you what it wrote and ask you to confirm before finishing.

**⚠️ Do this fully — including the final confirmation — before Step 5 (creating the scheduled task).** The scheduled task runs unattended, so if onboarding isn't finished first, there's no one there to answer its questions when it fires. If you need to pause partway through, that's fine — just come back and finish this step before moving on.

---

## Step 4 — (Optional but recommended) Set up live market data via LSEG

If you have an LSEG Workspace subscription:

1. Open LSEG Workspace and sign in
2. Search `APPKEY` to open the App Key Generator, create a key for a desktop application, select the **EDP API** and **Eikon Data API** scopes
3. Install the Python library:
   ```bash
   pip3 install --user lseg-data
   ```
4. In the sterling-workspace folder, create `lseg-data.config.json`:
   ```json
   {
       "sessions": {
           "default": "desktop.workspace",
           "desktop": {
               "workspace": {
                   "app-key": "YOUR_APP_KEY_HERE"
               }
           }
       }
   }
   ```
   (This file is already in `.gitignore` — it will never be pushed to GitHub.)
5. Test it (with Workspace open):
   ```bash
   cd ~/Documents/sterling-workspace
   python3 get_quote.py MSFT.O
   ```
   A price and P/E confirms it's working.
6. Set LSEG Workspace to launch at login (System Settings → Login Items on Mac, or Startup Apps on Windows), so it's running when the scheduled fetch fires.
7. Schedule the daily fetch to run ~15 minutes before your research task (see Step 6). On Mac, this is a `cron` job:
   ```bash
   crontab -e
   ```
   Add a line like:
   ```
   45 8 * * 1-5 cd /full/path/to/sterling-workspace && /usr/bin/python3 fetch_lseg.py >> /tmp/lseg-fetch.log 2>&1
   ```
   (adjust the path and time to match your setup)

If you skip this step entirely, Sterling will source all figures from the web and flag them as such — fully functional, just less precise than institutional data.

---

## Step 5 — Create the scheduled task

**Only do this once Step 3 (onboarding) is fully complete and confirmed.** Check that USER.md has no `[PLACEHOLDER]` markers left before proceeding.

1. In the Claude desktop app, click **Scheduled** in the sidebar
2. Click **New task**
3. Fill in the fields exactly as described in **`SCHEDULED-TASK-PROMPT.md`** — copy the prompt from that file
4. Save

---

## Step 6 — Verify

The next morning, check that the scheduled task ran and (if you set up LSEG) that the fetch ran too:

```bash
cat /tmp/lseg-fetch.log
head -3 ~/Documents/sterling-workspace/state/lseg-snapshot.md
```

---

## Using it day-to-day

See `sterling-how-it-works.md` for what Sterling does and how each call is structured. See `running-sterling-manually.md` for how to trigger runs on demand, refresh data, or feed it articles via the `inbox/` folder. See **`BACKUP.md`** for how to save your changes to GitHub.

---

## What's in this repo

| File / folder | Purpose |
|---|---|
| `SETUP.md` | This file |
| `BACKUP.md` | How to save your changes to GitHub |
| `SCHEDULED-TASK-PROMPT.md` | Exact text for the scheduled task |
| `ONBOARDING.md` | Tells the agent how to run the first-time interview |
| `DAILY-TASK.md` | What the agent does on every scheduled run |
| `SOUL.md` | Who Sterling is — mandate and hard boundaries |
| `IDENTITY.md` | Sterling's persona |
| `ANALYSIS.md` | The 8-step research method |
| `MONITORING.md` | The operating philosophy for the daily cycle |
| `AGENTS.md` | Standing operating rules |
| `USER.md` | The person's profile — starts with placeholders |
| `MEMORY.md` | Portfolio snapshot — starts empty/placeholders |
| `state/` | Living data — watchlist, theses, constraints, deployment plan, decision log |
| `inbox/` | Drop zone for articles/PDFs the user wants Sterling to read |
| `fetch_lseg.py` | Pulls live LSEG data for the watchlist |
| `get_quote.py` | On-demand LSEG price lookup |
