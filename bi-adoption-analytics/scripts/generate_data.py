"""
Generates a synthetic enterprise BI dataset for the
"Enterprise BI Dashboard Adoption & Support Analytics" project.

Period: 1 Apr 2026 to 30 Sep 2026 (6 months)
Output: CSV files in ../data/

Planted issues (things the analysis should find):
  1. Client Profitability report: failed loads spike after a data-source
     change on 15 Jun 2026.
  2. APAC access requests take much longer to resolve (single approver).
  3. Pipeline Tracker adoption in Sales falls after a UI change on 1 Jul 2026.
  4. Utilization Dashboard is slow to load (large dataset, no aggregation).
"""

import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
OUT = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT, exist_ok=True)

START, END = pd.Timestamp("2026-04-01"), pd.Timestamp("2026-09-30")
DAYS = pd.date_range(START, END, freq="D")
WORKDAYS = DAYS[DAYS.dayofweek < 5]

SOURCE_CHANGE = pd.Timestamp("2026-06-15")
UI_CHANGE = pd.Timestamp("2026-07-01")

# ---------------- Reports ----------------
reports = pd.DataFrame([
    ("R01", "Revenue Overview",       "Finance",    "Power BI", "Databricks"),
    ("R02", "Pipeline Tracker",       "Sales",      "Power BI", "Salesforce"),
    ("R03", "Headcount Planner",      "HR",         "Tableau",  "Workday"),
    ("R04", "Utilization Dashboard",  "Operations", "Power BI", "Databricks"),
    ("R05", "Client Profitability",   "Finance",    "Power BI", "Databricks"),
    ("R06", "Expense Monitor",        "Finance",    "Tableau",  "SAP"),
    ("R07", "Marketing Funnel",       "Marketing",  "Power BI", "HubSpot"),
    ("R08", "Ops KPI Scorecard",      "Operations", "Tableau",  "Databricks"),
], columns=["report_id", "report_name", "owner_team", "platform", "data_source"])

# ---------------- Users ----------------
N_USERS = 420
departments = ["Finance", "Sales", "Operations", "HR", "Marketing", "Strategy"]
dept_w = [0.20, 0.22, 0.20, 0.10, 0.12, 0.16]
regions = ["India", "North America", "Europe", "APAC"]
region_w = [0.30, 0.30, 0.25, 0.15]
roles = ["Analyst", "Manager", "Director", "Partner"]
role_w = [0.50, 0.30, 0.13, 0.07]

join_dates = pd.to_datetime(
    rng.choice(pd.date_range("2025-01-01", "2026-06-30"), N_USERS)
)
users = pd.DataFrame({
    "user_id": [f"U{i:04d}" for i in range(1, N_USERS + 1)],
    "department": rng.choice(departments, N_USERS, p=dept_w),
    "region": rng.choice(regions, N_USERS, p=region_w),
    "role": rng.choice(roles, N_USERS, p=role_w),
    "join_date": join_dates.date,
})

# Which reports each department mainly uses (weights over R01..R08)
dept_report_w = {
    "Finance":    [0.30, 0.02, 0.03, 0.05, 0.30, 0.25, 0.02, 0.03],
    "Sales":      [0.15, 0.60, 0.02, 0.03, 0.10, 0.02, 0.06, 0.02],
    "Operations": [0.05, 0.02, 0.08, 0.40, 0.05, 0.05, 0.02, 0.33],
    "HR":         [0.05, 0.02, 0.70, 0.10, 0.02, 0.05, 0.02, 0.04],
    "Marketing":  [0.10, 0.15, 0.02, 0.02, 0.03, 0.05, 0.60, 0.03],
    "Strategy":   [0.25, 0.10, 0.05, 0.10, 0.25, 0.05, 0.05, 0.15],
}
dept_daily_p = {"Finance": 0.55, "Sales": 0.45, "Operations": 0.50,
                "HR": 0.35, "Marketing": 0.40, "Strategy": 0.45}

base_load = {"R01": 3.5, "R02": 4.0, "R03": 3.0, "R04": 13.0,
             "R05": 5.0, "R06": 3.5, "R07": 4.0, "R08": 4.5}
base_fail = {"R01": 0.02, "R02": 0.025, "R03": 0.02, "R04": 0.04,
             "R05": 0.025, "R06": 0.02, "R07": 0.02, "R08": 0.03}

# ---------------- Usage log ----------------
rows = []
report_ids = reports["report_id"].tolist()
u_join = pd.to_datetime(users["join_date"]).values

# Per-user engagement: most users are light users, ~12% barely use BI at all
engagement = rng.beta(1.6, 2.4, N_USERS) * 1.6
engagement[rng.random(N_USERS) < 0.12] = 0.02

# Planted issue 3: ~40% of Sales users quit dashboards after the UI change
churn_date = {}
for i, u in users.iterrows():
    if u["department"] == "Sales" and rng.random() < 0.40:
        churn_date[i] = UI_CHANGE + pd.Timedelta(days=int(rng.integers(5, 75)))

for d in WORKDAYS:
    for i, u in users.iterrows():
        if u_join[i] > np.datetime64(d):
            continue
        if i in churn_date and d >= churn_date[i]:
            continue
        p = min(0.95, dept_daily_p[u["department"]] * engagement[i])
        if rng.random() > p:
            continue
        w = np.array(dept_report_w[u["department"]], dtype=float)
        # Remaining Sales users also open Pipeline Tracker less often
        if u["department"] == "Sales" and d >= UI_CHANGE:
            weeks_after = (d - UI_CHANGE).days / 7
            w[1] *= max(0.45, 1 - 0.05 * weeks_after)
        w = w / w.sum()
        n = rng.integers(1, 4)
        for rid in rng.choice(report_ids, size=n, replace=False, p=w):
            fail_p = base_fail[rid]
            load = base_load[rid]
            # Planted issue 1: Client Profitability breaks after source change
            if rid == "R05" and d >= SOURCE_CHANGE:
                fail_p = 0.19
                load *= 1.6
            failed = rng.random() < fail_p
            load_time = max(0.8, rng.normal(load, load * 0.25))
            if failed:
                load_time = round(rng.uniform(30, 60), 1)  # timeout
            rows.append((d.date(), u["user_id"], rid,
                         0 if failed else int(rng.integers(1, 4)),
                         round(load_time, 1),
                         "Failed" if failed else "Success"))

usage = pd.DataFrame(rows, columns=["date", "user_id", "report_id",
                                    "views", "load_time_sec", "load_status"])
usage.insert(0, "session_id", [f"S{i:06d}" for i in range(1, len(usage) + 1)])

# ---------------- Access requests ----------------
req_rows = []
n_req = 640
req_users = users.sample(n_req, replace=True, random_state=7).reset_index(drop=True)
for i, u in req_users.iterrows():
    d = pd.Timestamp(rng.choice(WORKDAYS))
    w = np.array(dept_report_w[u["department"]]); w = w / w.sum()
    rid = rng.choice(report_ids, p=w)
    # Planted issue 2: APAC has one approver, so slow
    if u["region"] == "APAC":
        days = max(1, int(rng.normal(9, 3)))
    else:
        days = max(0, int(rng.normal(2.2, 1.2)))
    resolved_on = d + pd.Timedelta(days=days)
    if resolved_on > END:
        status, resolved, days = "Pending", None, None
    else:
        status = "Approved" if rng.random() < 0.9 else "Rejected"
        resolved = resolved_on.date()
    req_rows.append((f"AR{i+1:04d}", u["user_id"], rid, d.date(),
                     resolved, status, days))
access = pd.DataFrame(req_rows, columns=["request_id", "user_id", "report_id",
                                         "request_date", "resolved_date",
                                         "status", "days_to_resolve"])
access["days_to_resolve"] = access["days_to_resolve"].astype("Int64")

# ---------------- Feedback (monthly pulse survey) ----------------
fb_rows = []
cats = ["Slow loading", "Wrong or missing data", "Access issues",
        "Confusing UI", "Missing feature", "No issue"]
usage["month"] = pd.to_datetime(usage["date"]).dt.to_period("M")
user_month = usage.groupby(["user_id", "month"]).agg(
    sessions=("session_id", "count"),
    fails=("load_status", lambda s: (s == "Failed").sum()),
    slow=("load_time_sec", lambda s: (s > 10).mean()),
    pipeline=("report_id", lambda s: (s == "R02").mean()),
).reset_index().merge(users[["user_id", "department", "region"]], on="user_id")

apac_users = set(users.loc[users.region == "APAC", "user_id"])
fid = 1
for _, r in user_month.iterrows():
    if rng.random() > 0.30:  # ~30% response rate
        continue
    fail_rate = r["fails"] / r["sessions"]
    score = 4.3 - 6 * fail_rate - 0.8 * r["slow"]
    cat_w = np.array([1 + 8 * r["slow"], 1 + 30 * fail_rate,
                      1 + (2.5 if r["user_id"] in apac_users else 0),
                      1, 0.8, 3.0])
    month_start = r["month"].to_timestamp()
    if r["department"] == "Sales" and month_start >= UI_CHANGE:
        score -= 0.9
        cat_w[3] += 5
    score = int(np.clip(round(rng.normal(score, 0.6)), 1, 5))
    if score >= 4:
        cat_w[5] += 4
    cat = rng.choice(cats, p=cat_w / cat_w.sum())
    day = month_start + pd.Timedelta(days=int(rng.integers(20, 27)))
    fb_rows.append((f"F{fid:05d}", r["user_id"], day.date(), score, cat))
    fid += 1
feedback = pd.DataFrame(fb_rows, columns=["response_id", "user_id", "date",
                                          "satisfaction", "issue_category"])

usage = usage.drop(columns="month")

# ---------------- Save ----------------
reports.to_csv(os.path.join(OUT, "reports.csv"), index=False)
users.to_csv(os.path.join(OUT, "users.csv"), index=False)
usage.to_csv(os.path.join(OUT, "usage_log.csv"), index=False)
access.to_csv(os.path.join(OUT, "access_requests.csv"), index=False)
feedback.to_csv(os.path.join(OUT, "feedback.csv"), index=False)

print("reports", len(reports), "| users", len(users), "| usage", len(usage),
      "| access", len(access), "| feedback", len(feedback))
