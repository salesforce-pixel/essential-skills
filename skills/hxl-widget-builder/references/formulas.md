# Formulas in Widgets

> ⚠️ **Don't use formulas over `$attrs` in widgets rendered through an MCP server (scenario C).** The MCP wrapper renderer rewrites plain `{!$attrs.x}` bindings to `$attrs.outputValues.<payload>.x`, but not `$attrs` references inside a formula. Every formula below that touches `$attrs` fails at render time. The client reports a crash quoting the half-rewritten expression, e.g. `{!$attrs.outputValues.snapshot.currencyCode} {!IF(NULLVALUE($attrs.amount, 0) …`. Verified in Claude web, 2026-09-21. For MCP widgets, compute the value in Apex and bind it plainly. Use this page for scenarios A/B only. Formulas over loop variables (`$opp.x`) weren't affected by the rewrite issue but are untested in MCP, so prefer Apex-computed item fields there too (e.g. `Opp.amountLabel`). `validate_hxl.py` fails `mcp-plain-bindings` when this rule is broken.

Widget expressions use a formula language based on the open-source Salesforce formula engine. A formula can appear anywhere a `{!...}` binding can: attribute values, string interpolation, and `meta.if`.

Rules:
- Function names and operators are UPPERCASE and case-sensitive.
- References inside formulas use the same paths as plain bindings (`$attrs.x`, loop vars inside `forEach`). Every reference must resolve.
- Inside `forEach`, formulas evaluate per item.
- Parse ISO date strings with `DATEVALUE` / `DATETIMEVALUE` / `TIMEVALUE` before date math.
- Scenarios A/B: a formula can replace a new schema attribute for a derived display value. Scenario C: add the attribute and compute it in Apex (see the warning above). Business logic always lives in Apex.
- Only use functions listed here (the validator flags anything else).

| Category | Supported |
|---|---|
| Arithmetic | `+ - * / ^` (parenthesize) |
| Comparison | `= <> > < >= <=` |
| Logical | `IF(c,a,b)`, `CASE(x, v1,r1, …, default)`, `AND(…)`, `OR(…)`, `NOT(x)`, `ISNULL(x)`, `ISBLANK(x)` |
| Text | `UPPER`, `LOWER`, `LEFT`, `RIGHT`, `MID` (1-based), `LEN`, `TRIM`, `REVERSE`, `SUBSTITUTE`, `FIND` (1-based), `LPAD`, `RPAD`, `TEXT`, `VALUE`, `CONTAINS`, `BEGINS`, `&` (concat) |
| Math | `MOD`, `MAX`, `MIN`, `ROUND(n,d)`, `ABS`, `SQRT`, `CEILING`, `FLOOR`, `MCEILING`, `MFLOOR`, `LOG`, `EXP`, `LN` |
| Date/time | `DATEVALUE`, `DATETIMEVALUE`, `TIMEVALUE`, `DAY`, `MONTH`, `YEAR`, `WEEKDAY` (1=Sun), `ADDMONTHS`, `TODAY()`, `NOW()`, `TIMENOW()`, `DATE(y,m,d)`, `HOUR`, `MINUTE`, `SECOND`, `MILLISECOND` |
| Null/encoding | `NULLVALUE(x,fb)`, `BLANKVALUE(x,fb)`, `HTMLENCODE`, `JSENCODE` |
| Pattern | `ISNUMBER`, `REGEX(str, pattern)` |

String literals: single quotes inside expressions (`'Won'`).

## Recipes

```text
Label/value with fallback     "{!BLANKVALUE($attrs.industry, 'Unknown industry')}"
Money in millions             "NOK {!TEXT(ROUND($attrs.annualRevenue / 1000000, 1))}M"
Status → badge variant        "{!CASE($opp.stageName, 'Closed Won', 'success', 'Closed Lost', 'error', 'info')}"
Threshold flag (meta.if)      "{!$attrs.openCaseCount > 5}"
Combined condition            "{!AND($attrs.isAtRisk, NOT(ISBLANK($attrs.ownerName)))}"
Truncate long text            "{!IF(LEN($attrs.summary) > 140, LEFT($attrs.summary, 140) & '…', $attrs.summary)}"
Close month from ISO string   "{!MONTH(DATEVALUE($opp.closeDate))}/{!YEAR(DATEVALUE($opp.closeDate))}"
Row number in loop            "{!$i + 1}."
```

Guard numeric math against nulls (`NULLVALUE($attrs.amount, 0)`), since the source data may omit a field.
