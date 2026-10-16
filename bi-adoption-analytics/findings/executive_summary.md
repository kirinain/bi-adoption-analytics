# Executive Summary: BI Portfolio Health Review (Apr to Sep 2026)

**Scope:** 8 enterprise reports (Power BI and Tableau), 420 licensed users, 6 departments, 4 regions.
**Data:** 26,576 report sessions, 640 access requests, 613 survey responses (30% response rate).
**Note:** All data is synthetic, built to simulate a real BI support environment.

## Headline

Adoption grew until July, then fell. Monthly active users (MAU) peaked at **365 in July** and dropped to **332 in September (-9%)**. Average satisfaction fell from **4.07 to 3.66** (out of 5) between April and August. Four issues explain most of the decline.

## Top 4 issues

| # | Issue | Evidence | Likely root cause | Recommended action | Priority |
|---|-------|----------|-------------------|--------------------|----------|
| 1 | Client Profitability fails to load | Failed loads jumped from **3.1% to 19.4%** after 15 Jun; **500 failed sessions** since; load time 5.0s to 8.0s | Data-source change on 15 Jun (query now times out on Databricks) | Escalate to data engineering: roll back or optimise the query; add a refresh-failure alert | P1 |
| 2 | Sales stopped using Pipeline Tracker | Sales MAU fell **70 to 47 (-33%)** Jun to Sep; Pipeline Tracker sessions **-39%**; Sales CSAT **4.10 to 2.75**; "Confusing UI" is **39%** of Sales feedback after July | 1 Jul UI redesign of Pipeline Tracker | Run 5 to 6 user interviews with Sales; restore key views or add a quick guide; re-test with users | P1 |
| 3 | APAC access requests are slow | APAC avg **8.7 days** to resolve vs **~1.7 days** elsewhere; only **4%** meet the 3-day SLA vs **90%+** for other regions; APAC users flag access issues **2.4x** more | Single approver for APAC | Add a backup approver; auto-escalate requests older than 3 days | P2 |
| 4 | Utilization Dashboard is slow | Avg load **13.1s**; **82%** of loads take over 10s (other reports: 3 to 7s) | Large unaggregated dataset | Request an aggregated table or incremental refresh from the platform team | P3 |

## Also worth noting

- **16 of 420 licensed users (4%)** never opened a report. These licences could be reviewed or the users onboarded.
- "Slow loading" (15%) and "Wrong or missing data" (14%) are the top complaint types across all users.

## Next steps

1. This week: escalate Issue 1 to data engineering and confirm the 15 Jun change log.
2. Next 2 weeks: Sales interviews for Issue 2; draft enhancement request (see `user_stories_and_test_cases.md`).
3. Ops: agree a backup APAC approver with the platform admin.
4. Track MAU, failed-load %, SLA % and CSAT monthly on the dashboard to confirm the fixes worked.
