# Data Dictionary

Period covered: 1 Apr 2026 to 30 Sep 2026. Usage is logged on working days only.

## users.csv (420 rows, dimension)

| Column | Type | Description |
|--------|------|-------------|
| user_id | text | Unique user ID (U0001 to U0420) |
| department | text | Finance, Sales, Operations, HR, Marketing, Strategy |
| region | text | India, North America, Europe, APAC |
| role | text | Analyst, Manager, Director, Partner |
| join_date | date | Date the user got a BI licence |

## reports.csv (8 rows, dimension)

| Column | Type | Description |
|--------|------|-------------|
| report_id | text | R01 to R08 |
| report_name | text | Report title |
| owner_team | text | Business team that owns the report |
| platform | text | Power BI or Tableau |
| data_source | text | Source system (Databricks, Salesforce, Workday, SAP, HubSpot) |

## usage_log.csv (26,576 rows, fact)

One row per report session (a user opening a report).

| Column | Type | Description |
|--------|------|-------------|
| session_id | text | Unique session ID |
| date | date | Session date |
| user_id | text | Links to users |
| report_id | text | Links to reports |
| views | integer | Pages viewed in the session (0 if the load failed) |
| load_time_sec | decimal | Seconds to load. Failed loads show the timeout time (30 to 60s) |
| load_status | text | Success or Failed |

## access_requests.csv (640 rows, fact)

| Column | Type | Description |
|--------|------|-------------|
| request_id | text | Unique request ID |
| user_id | text | Who asked for access |
| report_id | text | Report requested |
| request_date | date | Date raised |
| resolved_date | date | Date approved or rejected (blank if pending) |
| status | text | Approved, Rejected, Pending |
| days_to_resolve | integer | Calendar days from request to resolution (blank if pending) |

## feedback.csv (613 rows, fact)

Monthly pulse survey. About 30% of active users respond each month.

| Column | Type | Description |
|--------|------|-------------|
| response_id | text | Unique response ID |
| user_id | text | Respondent |
| date | date | Response date |
| satisfaction | integer | 1 (very unhappy) to 5 (very happy) |
| issue_category | text | Main issue: Slow loading, Wrong or missing data, Access issues, Confusing UI, Missing feature, No issue |

## Known events (for context)

| Date | Event |
|------|-------|
| 15 Jun 2026 | Client Profitability data source query changed |
| 1 Jul 2026 | Pipeline Tracker UI redesign released |
