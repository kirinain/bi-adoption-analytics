# Issue Triage Backlog

How items are prioritised:
- **Impact:** how many users are affected and how badly (High / Medium / Low)
- **Effort:** rough work needed to fix (High / Medium / Low)
- **Priority:** P1 = fix now, P2 = this sprint, P3 = plan for next quarter

| ID | Type | Item | Users affected | Impact | Effort | Priority | Escalate to | Status | Dependency |
|----|------|------|----------------|--------|--------|----------|-------------|--------|------------|
| BL-01 | Incident | Client Profitability failed loads at 19.4% since 15 Jun | Finance, Strategy | High | Medium | **P1** | Data engineering (Databricks) | Escalated | Change log for 15 Jun source change |
| BL-02 | Enhancement | Pipeline Tracker UI: restore key views lost in 1 Jul redesign | Sales (70 users) | High | Medium | **P1** | BI developer + Sales lead | Requirements | User interviews (BL-05) |
| BL-03 | Process | APAC access approvals take 8.7 days avg | APAC (all depts) | Medium | Low | **P2** | Platform admin | Proposed | Backup approver nominated |
| BL-04 | Enhancement | Add refresh-failure alert for all Databricks reports | All Databricks report users | Medium | Low | **P2** | Data engineering | Backlog | BL-01 fix |
| BL-05 | Research | 5 to 6 interviews with Sales users on Pipeline Tracker | Sales | Medium | Low | **P2** | Product (self) | In progress | None |
| BL-06 | Enhancement | Utilization Dashboard: aggregated table / incremental refresh | Operations, Strategy | Medium | High | **P3** | Platform team | Backlog | Data model change |
| BL-07 | Hygiene | Review 16 licensed users who never opened a report | 16 users | Low | Low | **P3** | Platform admin | Backlog | Manager confirmation |

## Escalation notes

- **BL-01:** Shared session IDs of failed loads (timeouts at 30 to 60s) and the before/after failure rate with data engineering. Asked for the exact query change made on 15 Jun.
- **BL-03:** Root cause is process, not technical. One approver covers APAC, so requests wait during their leave or busy weeks.

## Trade-offs to communicate

- Fixing BL-02 quickly (rolling back the redesign) restores adoption but loses the new features some managers asked for. A middle path is restoring the 2 to 3 most-used views and keeping the rest.
- BL-06 needs a data model change, which risks breaking other reports that share the dataset. It needs full regression testing (see test cases).
