"""
Computes the headline numbers used in findings/executive_summary.md.
Run after generate_data.py. These should match what the Power BI
dashboard shows (use them as a reconciliation check).
"""

import os
import pandas as pd

D = os.path.join(os.path.dirname(__file__), "..", "data")
users = pd.read_csv(os.path.join(D, "users.csv"))
reports = pd.read_csv(os.path.join(D, "reports.csv"))
usage = pd.read_csv(os.path.join(D, "usage_log.csv"), parse_dates=["date"])
access = pd.read_csv(os.path.join(D, "access_requests.csv"),
                     parse_dates=["request_date", "resolved_date"])
fb = pd.read_csv(os.path.join(D, "feedback.csv"), parse_dates=["date"])

usage = usage.merge(users, on="user_id").merge(reports, on="report_id")
usage["month"] = usage["date"].dt.to_period("M")
usage["failed"] = usage["load_status"].eq("Failed")

print("=== Overall ===")
print("Sessions:", len(usage))
print("Users who opened a report:", usage.user_id.nunique(), "of", len(users))
print("Overall failed-load %:", round(usage.failed.mean() * 100, 2))
print("Avg load time (successful):",
      round(usage.loc[~usage.failed, "load_time_sec"].mean(), 1))

print("\n=== Monthly active users ===")
print(usage.groupby("month").user_id.nunique())

print("\n=== Failed-load % by report ===")
print((usage.groupby("report_name").failed.mean() * 100).round(2)
      .sort_values(ascending=False))

cp = usage[usage.report_id == "R05"]
pre = cp[cp.date < "2026-06-15"]; post = cp[cp.date >= "2026-06-15"]
print("\n=== Client Profitability before/after 15 Jun ===")
print("Failed % before:", round(pre.failed.mean() * 100, 2),
      "| after:", round(post.failed.mean() * 100, 2))
print("Avg load (success) before:",
      round(pre.loc[~pre.failed, "load_time_sec"].mean(), 1),
      "| after:", round(post.loc[~post.failed, "load_time_sec"].mean(), 1))
print("Failed sessions after change:", int(post.failed.sum()))

print("\n=== Avg load time (successful) by report ===")
print(usage[~usage.failed].groupby("report_name").load_time_sec.mean()
      .round(1).sort_values(ascending=False))
r04 = usage[(usage.report_id == "R04") & ~usage.failed]
print("Utilization Dashboard loads > 10s %:",
      round((r04.load_time_sec > 10).mean() * 100, 1))

print("\n=== Access requests ===")
a = access.merge(users[["user_id", "region"]], on="user_id")
print(a.status.value_counts())
print("Avg days to resolve by region:")
print(a.groupby("region").days_to_resolve.mean().round(1))
print("Median by region:")
print(a.groupby("region").days_to_resolve.median())
print("Pending by region:")
print(a[a.status == "Pending"].region.value_counts())
print("SLA (<=3 days) met % by region:")
res = a.dropna(subset=["days_to_resolve"])
print((res.groupby("region").days_to_resolve.apply(lambda s: (s <= 3).mean())
       * 100).round(1))

print("\n=== Sales + Pipeline Tracker ===")
sales = usage[usage.department == "Sales"]
print("Sales MAU by month:")
print(sales.groupby("month").user_id.nunique())
print("Pipeline Tracker sessions by Sales, by month:")
print(sales[sales.report_id == "R02"].groupby("month").size())
jun = sales[(sales.month == "2026-06")]
sep = sales[(sales.month == "2026-09")]
print("Sales MAU Jun -> Sep:", jun.user_id.nunique(), "->", sep.user_id.nunique())
print("PT sessions Jun -> Sep:", (jun.report_id == "R02").sum(), "->",
      (sep.report_id == "R02").sum())

print("\n=== Feedback ===")
fb = fb.merge(users[["user_id", "department", "region"]], on="user_id")
fb["month"] = fb.date.dt.to_period("M")
print("Responses:", len(fb), "| Avg CSAT:", round(fb.satisfaction.mean(), 2))
print("CSAT by month:")
print(fb.groupby("month").satisfaction.mean().round(2))
print("Sales CSAT by month:")
print(fb[fb.department == "Sales"].groupby("month").satisfaction.mean().round(2))
print("Issue categories (all):")
print(fb.issue_category.value_counts(normalize=True).mul(100).round(1))
print("Sales issue categories Jul-Sep:")
s = fb[(fb.department == "Sales") & (fb.date >= "2026-07-01")]
print(s.issue_category.value_counts(normalize=True).mul(100).round(1))
print("APAC 'Access issues' % vs others:",
      round((fb[fb.region == "APAC"].issue_category == "Access issues").mean() * 100, 1),
      round((fb[fb.region != "APAC"].issue_category == "Access issues").mean() * 100, 1))
print("Response rate (responses / active user-months):",
      round(len(fb) / usage.groupby(["user_id", "month"]).ngroups * 100, 1))
