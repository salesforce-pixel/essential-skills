# Query Agentforce Coworker Usage and Adoption Data in Data 360

Measure Agentforce Coworker adoption by querying the AI Agent Generative AI Usage data model object (DMO) in Data 360. Find active users, adoption rate, and usage trends, or build a Data 360 report.

| **REQUIRED EDITIONS AND PERMISSIONS**                |                                                                                                                                                              |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Available in:                                        | Enterprise, Unlimited, and Agentforce 1 Editions                                                                                                             |
| To query Agentforce Coworker usage data in Data 360: | See permissions table in [Create and Run Queries in Query Editor](https://help.salesforce.com/s/articleView?id=data.c360_a_query_editor_create_queries.htm). |

The AI Agent Generative AI Usage DMO (`AiAgentGenerativeAiUsage_std__dlm`) records each Agentforce Coworker request with the user ID and a timestamp. To filter for Agentforce Coworker, use `GenAiGatewayFeatureName__c = 'AgentforceCoworker'`.

## Build a Data 360 Report on Agentforce Coworker Usage

1. Create a Data 360 report with the **AI Agent Generative AI Usage** report type.
2. Add a filter where **Feature Name** equals `AgentforceCoworker`.

:::note
The AI Agent Generative AI Usage DMO includes user IDs but not user names, and Data 360 reports don't support joined reports. To group a report by user name, create a data transform that joins the AI Agent Generative AI Usage DMO with the User DMO. Write the output to a custom DMO, and then build the report on the custom DMO.
:::

To review how the large language model (LLM) responds, query the Einstein Audit and Feedback DMOs. See [Review Agentforce Coworker Responses in Data 360](https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-query-audit-trail.md).

## Query Agentforce Coworker Usage in Query Editor

1. In Data 360, open **Query Editor**.
2. Enter one of the example queries in this topic.
3. Run the query.

## Example Queries for Agentforce Coworker Adoption

### Track Agentforce Coworker Usage by User and Date

Count Agentforce Coworker requests for each user on each day.

```sql
-- Agentforce Coworker Usage by User by Date
SELECT
    "UserId__c",
    CAST("Timestamp__c" AS DATE) AS "UsageDate",
    COUNT(*) AS "QueryCount"
FROM "AiAgentGenerativeAiUsage_std__dlm"
WHERE "GenAiGatewayFeatureName__c" = 'AgentforceCoworker'
GROUP BY "UserId__c", CAST("Timestamp__c" AS DATE)
ORDER BY "UsageDate" DESC, "QueryCount" DESC
```

### Track Agentforce Coworker Usage by Date

Count Agentforce Coworker requests for each day across all users.

```sql
-- Agentforce Coworker Usage by Date
SELECT
    CAST("Timestamp__c" AS DATE) AS "UsageDate",
    COUNT(*) AS "QueryCount"
FROM "AiAgentGenerativeAiUsage_std__dlm"
WHERE "GenAiGatewayFeatureName__c" = 'AgentforceCoworker'
GROUP BY CAST("Timestamp__c" AS DATE)
ORDER BY "UsageDate" DESC, "QueryCount" DESC
```

### Calculate the Agentforce Coworker Adoption Rate

Find the percentage of licensed users who made at least one Agentforce Coworker request. Replace `200` with your licensed seat count in both places.

```sql
-- What share of the people I've licensed are actually using Agentforce Coworker?
SELECT
    200                                                        AS total_licensed_users, -- replace with your actual seat count
    COUNT(DISTINCT UserId__c)                                  AS active_users,
    ROUND(
        COUNT(DISTINCT UserId__c) * 100.0 / 200             -- replace with your actual seat count
    , 1)                                                       AS adoption_rate_pct
FROM AiAgentGenerativeAiUsage_std__dlm
WHERE GenAiGatewayFeatureName__c = 'AgentforceCoworker'
```

### Check Agentforce Coworker Health for the Last 30 Days

See total prompts, unique active users, average prompts per day, and first and last usage dates for the last 30 days.

```sql
-- What is the overall health of Agentforce Coworker at my company?
SELECT
    COUNT(*)                                                   AS total_prompts,
    COUNT(DISTINCT UserId__c)                                  AS active_users,
    ROUND(COUNT(*) * 1.0 / 30, 1)                             AS avg_prompts_per_day,
    MIN(CAST(Timestamp__c AS DATE))                            AS first_usage_date,
    MAX(CAST(Timestamp__c AS DATE))                            AS last_usage_date
FROM AiAgentGenerativeAiUsage_std__dlm
WHERE GenAiGatewayFeatureName__c = 'AgentforceCoworker'
  AND Timestamp__c >= CURRENT_DATE - INTERVAL '30' DAY
```

### Count Active Agentforce Coworker Users Over 7, 30, and 90 Days

Compare distinct active users across three time windows to see whether adoption is growing or leveling off.

```sql
-- How many users are actively using Agentforce Coworker?
SELECT
    'Last 7 days'                                              AS period,
    COUNT(DISTINCT UserId__c)                                  AS active_users
FROM AiAgentGenerativeAiUsage_std__dlm
WHERE GenAiGatewayFeatureName__c = 'AgentforceCoworker'
  AND Timestamp__c >= CURRENT_DATE - INTERVAL '7' DAY

UNION ALL

SELECT
    'Last 30 days',
    COUNT(DISTINCT UserId__c)
FROM AiAgentGenerativeAiUsage_std__dlm
WHERE GenAiGatewayFeatureName__c = 'AgentforceCoworker'
  AND Timestamp__c >= CURRENT_DATE - INTERVAL '30' DAY

UNION ALL

SELECT
    'Last 90 days',
    COUNT(DISTINCT UserId__c)
FROM AiAgentGenerativeAiUsage_std__dlm
WHERE GenAiGatewayFeatureName__c = 'AgentforceCoworker'
  AND Timestamp__c >= CURRENT_DATE - INTERVAL '90' DAY
```

### Measure Agentforce Coworker Usage per User

Break down each user's total prompts, active days, and average prompts per active day. Use the results to find your most active users and the users who need more training.

```sql
-- How intensively is each active user using Agentforce Coworker?
SELECT
    UserId__c                                                  AS user_id,
    COUNT(*)                                                   AS total_prompts,
    COUNT(DISTINCT CAST(Timestamp__c AS DATE))                 AS active_days,
    ROUND(COUNT(*) * 1.0
        / NULLIF(COUNT(DISTINCT CAST(Timestamp__c AS DATE)), 0)
    , 1)                                                       AS avg_prompts_per_active_day,
    MIN(CAST(Timestamp__c AS DATE))                            AS first_seen,
    MAX(CAST(Timestamp__c AS DATE))                            AS last_seen
FROM AiAgentGenerativeAiUsage_std__dlm
WHERE GenAiGatewayFeatureName__c = 'AgentforceCoworker'
GROUP BY UserId__c
ORDER BY total_prompts DESC
```
