# DAX Measures

Create a table called `_Measures` (Home > Enter data > empty table) and add these measures to it, so they are easy to find.

## Date table

Modeling > New table:

```dax
Date =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2026, 4, 1 ), DATE ( 2026, 9, 30 ) ),
    "Month", FORMAT ( [Date], "YYYY-MM" ),
    "Month Name", FORMAT ( [Date], "MMM YYYY" ),
    "Week Start", [Date] - WEEKDAY ( [Date], 2 ) + 1
)
```

Then: right-click the `Date` table > Mark as date table > choose `Date[Date]`.

## Adoption

```dax
Sessions = COUNTROWS ( usage_log )

Active Users = DISTINCTCOUNT ( usage_log[user_id] )

Licensed Users = COUNTROWS ( users )

Adoption % = DIVIDE ( [Active Users], [Licensed Users] )

MAU MoM % =
VAR CurrentMAU = [Active Users]
VAR PrevMAU =
    CALCULATE ( [Active Users], DATEADD ( 'Date'[Date], -1, MONTH ) )
RETURN
    DIVIDE ( CurrentMAU - PrevMAU, PrevMAU )

Never Active Users =
COUNTROWS (
    FILTER ( users, CALCULATE ( COUNTROWS ( usage_log ) ) = 0 )
)
```

## Reliability and performance

```dax
Failed Loads =
CALCULATE ( [Sessions], usage_log[load_status] = "Failed" )

Failed Load % = DIVIDE ( [Failed Loads], [Sessions] )

Avg Load Time (s) =
CALCULATE (
    AVERAGE ( usage_log[load_time_sec] ),
    usage_log[load_status] = "Success"
)

Slow Load % =
DIVIDE (
    CALCULATE (
        [Sessions],
        usage_log[load_status] = "Success",
        usage_log[load_time_sec] > 10
    ),
    CALCULATE ( [Sessions], usage_log[load_status] = "Success" )
)
```

## Access requests (support)

```dax
Access Requests = COUNTROWS ( access_requests )

Pending Requests =
CALCULATE ( [Access Requests], access_requests[status] = "Pending" )

Avg Days to Resolve = AVERAGE ( access_requests[days_to_resolve] )

SLA Met % =
DIVIDE (
    CALCULATE ( [Access Requests], access_requests[days_to_resolve] <= 3 ),
    CALCULATE (
        [Access Requests],
        NOT ISBLANK ( access_requests[days_to_resolve] )
    )
)
```

## Feedback

```dax
Survey Responses = COUNTROWS ( feedback )

Avg CSAT = AVERAGE ( feedback[satisfaction] )

Issue Share % =
DIVIDE (
    [Survey Responses],
    CALCULATE ( [Survey Responses], ALL ( feedback[issue_category] ) )
)
```

## Formatting

- Set `Adoption %`, `MAU MoM %`, `Failed Load %`, `Slow Load %`, `SLA Met %`, `Issue Share %` to Percentage, 1 decimal.
- Set `Avg Load Time (s)`, `Avg Days to Resolve`, `Avg CSAT` to Decimal, 1 or 2 decimals.
