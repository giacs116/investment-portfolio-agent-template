# BACKUP.md — Saving Your Changes to GitHub

As Sterling works, it writes to files in this folder — the watchlist, decision log, theses, and more. None of that is automatically backed up. This guide covers how to save it.

---

## The three commands

Open Terminal (Mac) or PowerShell (Windows), go to this folder, and run:

```bash
cd ~/Documents/sterling-workspace
git add -A
git commit -m "Describe what changed"
git push
```

**What each does:**
- `git add -A` — gathers up everything that changed
- `git commit -m "..."` — saves a snapshot with a short label (write anything descriptive between the quotes — it's just a note for yourself)
- `git push` — uploads that snapshot to GitHub

Run all three together, one after another, whenever you want to back up.

---

## When to do this

- After a scheduled run, if you want that day's research and decision log entries saved
- After onboarding, once your files are filled in
- After any conversation where you asked Sterling to change a file (add a name to the watchlist, adjust a setting, etc.)
- Whenever you think of it — there's no harm in running it often

---

## The first time — you'll need to log in

The first time you push, GitHub will ask for a username and password. **It will not accept your regular GitHub password** — you need a Personal Access Token instead:

1. On github.com: click your profile picture → **Settings** → **Developer settings** (bottom of the left sidebar) → **Personal access tokens** → **Tokens (classic)**
2. **Generate new token (classic)**
3. Give it a name, check the **`repo`** box, generate
4. **Copy the token immediately** — it's shown only once
5. When Terminal asks for a password, paste the token (not your GitHub password)

To avoid re-entering it every time, run this once:
```bash
git config --global credential.helper store
```
(Mac users can use `osxkeychain` instead of `store` for better security: `git config --global credential.helper osxkeychain`)

---

## Checking what's changed before you commit

If you're curious what Sterling has modified since your last backup:
```bash
git status
```
This lists every file that's changed. Nothing here is destructive — it's just a preview.

---

## A note on privacy

This repository likely contains real financial information once it's set up (your portfolio, holdings, goals). **Keep the GitHub repository private** — never make it public. Check this under the repo's Settings → General on github.com if you're ever unsure.
