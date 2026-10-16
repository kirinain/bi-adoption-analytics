# Enterprise BI Dashboard Adoption & Support Analytics

A product operations case study on a portfolio of 8 enterprise BI reports (Power BI and Tableau) used by 420 people across 6 departments and 4 regions.

The goal: act as the analyst who owns these products. Track usage and adoption, find what is hurting users, trace root causes, and turn the findings into prioritised enhancement requests with test cases.

> All data is **synthetic**. It was generated with `scripts/generate_data.py` to simulate a realistic BI support environment, with a few real-world style problems planted in it.

![Adoption overview](screenshots/01_adoption.png)

## Key findings

| Issue | What the data shows | Root cause | Action |
|-------|--------------------|------------|--------|
| Client Profitability failing | Failed loads **3.1% → 19.4%** after 15 Jun; 500 failed sessions | Data-source change on 15 Jun | Escalated to data engineering (P1) |
| Sales leaving Pipeline Tracker | Sales MAU **70 → 47 (-33%)**; CSAT **4.10 → 2.75**; "Confusing UI" 39% of Sales feedback | 1 Jul UI redesign | Enhancement request + user interviews (P1) |
| Slow APAC access approvals | **8.7 days** avg vs ~1.7 elsewhere; **4%** meet 3-day SLA | Single approver | Backup approver + auto-escalation (P2) |
| Slow Utilization Dashboard | **13.1s** avg load; 82% of loads over 10s | Large unaggregated dataset | Aggregated table request (P3) |

Overall: MAU peaked at **365 in July** and fell to **332 in September**. Average satisfaction fell from **4.07 to 3.66** between April and August.

Full write-up: [`findings/executive_summary.md`](findings/executive_summary.md)

## Dashboard pages

| Page | What it answers |
|------|-----------------|
| Adoption Overview | Who uses which reports, and is usage growing? |
| Reliability & Performance | Which reports fail or load slowly, and since when? |
| Access & Support | How fast do access requests get resolved, by region? |
| User Feedback | How satisfied are users, and what do they complain about? |

Screenshots are in [`screenshots/`](screenshots/). The `.pbix` file is in [`dashboard/`](dashboard/).

## What's in this repo

```
data/                      Synthetic CSVs (users, reports, usage_log, access_requests, feedback)
scripts/generate_data.py   Builds the dataset (fixed seed, fully reproducible)
scripts/analyse.py         Computes the headline numbers (used to reconcile the dashboard)
dashboard/                 Power BI file (.pbix) and PDF export
docs/data_dictionary.md    Every table and column explained
docs/dax_measures.md       All DAX measures used in the dashboard
docs/powerbi_build_guide.md  How the dashboard was built, page by page
findings/executive_summary.md          Top issues, root causes, recommended actions
findings/issue_triage_backlog.md       Prioritised backlog with escalation owners and dependencies
findings/user_stories_and_test_cases.md  User stories, acceptance criteria, functional /
                                         permissions / data-reconciliation / regression tests,
                                         and an access-request process flow
findings/analysis_output.txt           Raw numbers from analyse.py
```

## Data model

Star schema with 3 fact tables and 3 dimensions:

- **Facts:** `usage_log` (26,576 sessions), `access_requests` (640), `feedback` (613 survey responses)
- **Dimensions:** `users` (420), `reports` (8), `Date`

See [`docs/data_dictionary.md`](docs/data_dictionary.md).

## How to reproduce

```bash
pip install -r requirements.txt
python scripts/generate_data.py   # writes CSVs to data/
python scripts/analyse.py         # prints headline numbers
```

Then open `dashboard/bi_adoption_dashboard.pbix` in Power BI Desktop, or follow [`docs/powerbi_build_guide.md`](docs/powerbi_build_guide.md) to rebuild it.

## Tools

Power BI (DAX, Power Query, star-schema modelling), Python (pandas, numpy), Excel, Markdown / Mermaid for documentation.
