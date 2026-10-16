# Power BI Build Guide

Time needed: about 1.5 to 2 hours. Power BI Desktop is free (Windows only).

## 1. Load the data (10 min)

1. Home > Get data > Text/CSV. Load all 5 files from `/data`.
2. In Power Query (Transform data), check column types:
   - `date`, `join_date`, `request_date`, `resolved_date` → Date
   - `load_time_sec` → Decimal number
   - `views`, `satisfaction`, `days_to_resolve` → Whole number
3. Close & Apply.

## 2. Build the model (10 min)

Create the `Date` table from `dax_measures.md`, then set these relationships in Model view (all one-to-many, single direction):

| From (one side) | To (many side) |
|-----------------|----------------|
| `users[user_id]` | `usage_log[user_id]`, `access_requests[user_id]`, `feedback[user_id]` |
| `reports[report_id]` | `usage_log[report_id]`, `access_requests[report_id]` |
| `Date[Date]` | `usage_log[date]`, `access_requests[request_date]`, `feedback[date]` |

This is a star schema: 3 fact tables (usage, access, feedback) and 3 dimensions (users, reports, date). Take a screenshot of Model view for the repo.

## 3. Add measures (15 min)

Copy all measures from `dax_measures.md`.

## 4. Build the pages (45 to 60 min)

Put these slicers on every page (use View > Sync slicers): **Month**, **Department**, **Region**, **Platform**.

### Page 1: Adoption Overview
- KPI cards: `Active Users`, `Adoption %`, `Sessions`, `Avg CSAT`, `Never Active Users`
- Line chart: `Active Users` by `Date[Month]` (shows the July peak and drop)
- Clustered bar: `Active Users` by `users[department]`
- Matrix: `report_name` rows, `Date[Month]` columns, `Sessions` values (add conditional formatting background color)

### Page 2: Reliability & Performance
- KPI cards: `Failed Load %`, `Avg Load Time (s)`, `Slow Load %`
- Bar chart: `Failed Load %` by `report_name` (sorted desc; Client Profitability stands out)
- Line chart: `Failed Load %` by `Date[Week Start]`, filtered to Client Profitability (shows the 15 Jun jump). Add a constant line or text box marking "Data source change, 15 Jun".
- Bar chart: `Avg Load Time (s)` by `report_name` (Utilization Dashboard stands out)

### Page 3: Access & Support
- KPI cards: `Access Requests`, `Pending Requests`, `Avg Days to Resolve`, `SLA Met %`
- Bar chart: `Avg Days to Resolve` by `users[region]` (APAC stands out)
- Bar chart: `SLA Met %` by `users[region]`
- Table: pending requests (request_id, user, region, report, request_date)

### Page 4: User Feedback
- KPI cards: `Survey Responses`, `Avg CSAT`
- Line chart: `Avg CSAT` by `Date[Month]`, with `users[department]` as legend (Sales drops after July)
- Stacked bar: `Issue Share %` by `issue_category`
- Use the Sales filter to show "Confusing UI" rising after July

### Page 5: Findings (optional but strong)
- A text page with the 4 issues from `findings/executive_summary.md` and a small visual next to each.

## 5. Check numbers match (reconciliation, 10 min)

With no filters applied, the dashboard should show:

| Check | Expected |
|-------|----------|
| Sessions | 26,576 |
| Licensed users | 420 |
| Never active users | 16 |
| Overall failed-load % | 4.1% |
| MAU July / September | 365 / 332 |
| Client Profitability failed-load % (whole period) | 13.0% |
| APAC avg days to resolve | 8.7 |
| Avg CSAT | 3.85 |
| Survey responses | 613 |

Full list: `findings/analysis_output.txt`. If a number is off, check data types and relationships first.

## 6. Polish and publish (15 min)

1. Use one consistent theme (View > Themes) and clear titles on every visual.
2. Save as `dashboard/bi_adoption_dashboard.pbix`.
3. Take a full screenshot of each page, save to `screenshots/` as `01_adoption.png`, `02_reliability.png`, `03_access.png`, `04_feedback.png`, `05_model.png`.
4. Optional: File > Export > Export to PDF and save to `dashboard/`.
5. Optional: Publish to web (needs a work or school account). If you can't, screenshots + .pbix are enough.
