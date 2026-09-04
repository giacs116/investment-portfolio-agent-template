# SCHEDULED-TASK-PROMPT.md

This is the exact text to paste into the **Prompt / Description** field when creating the scheduled task in Cowork. Copy everything in the box below.

---

## Task settings to use

| Field | Value |
|---|---|
| Name | Sterling Daily Research |
| Folder | This workspace folder (wherever you cloned/placed it) |
| Model | Sonnet |
| Approval | Automatically approve |
| Frequency | Weekdays, 9:00 AM (or your preferred time) |

---

## Prompt to paste

```
Read and follow DAILY-TASK.md in this folder exactly, in order. It tells you whether to run the onboarding check or the research cycle today.
```

That's the entire prompt. All the actual logic — onboarding-check-first, research-second, the breadth/depth structure, the cost limits — lives in `DAILY-TASK.md`, so this prompt never needs to change. If you want to adjust how the daily run works later, edit `DAILY-TASK.md`, not this prompt.
