# Running Data 360 SQL from Apex (`sfsqlquery`)

Verified 2026-10-06 in a sandbox on API 67.0: `hybrid_search()` with joins, `GROUP BY` and autodrop JSON runs
from Apex in about 0.5 s wall-clock, with about 30–100 ms of CPU and **0 callouts**.

Docs: [Query Data 360 Data with Apex](https://developer.salesforce.com/docs/data/data-cloud-query-guide/guide/dc-apex-query.md)
and the [sfsqlquery namespace](https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_namespace_sfsqlquery.htm).

## Which API

| API | Use |
|---|---|
| **`sfsqlquery`** (`SqlStatement` → `SqlRowIterator` → `Row`) | **Recommended for new code.** Typed accessors, a built-in test mock (`SqlTester`), and `SqlQueueable` for large results. |
| `ConnectApi.CdpQuery.queryAnsiSqlV2` | Low-level legacy interface; also works. Rows come back as `List<Object>` with a separate metadata map. |

Queries run with the **running user's** session and permissions.

## Synchronous query

```apex
sfsqlquery.SqlRowIterator rows = sfsqlquery.SqlStatement.create(sqlText, 'default').withWorkloadName('my_retriever').execute();
for (sfsqlquery.Row row : rows) {
    String chunk = row.getString('Chunk__c');
    Decimal score = row.getDecimal('Score__c');
}
```

- The second argument is the **data space** API name (usually `default`; it's shown on the search index page).
- Keep `SqlStatement.create(` on one line when chaining. The docs call this out.
- `withWorkloadName()` labels the query for Salesforce Support. Set it.
- The query is submitted when iteration starts. The iterator is single-use.
- `Row` accessors: `getString`, `getDecimal`, `getDouble`, `getInteger`, `getBoolean`, `getDate`, `getDateTime`, `getObject`, by column name or 0-based index. An **unknown column name throws `IllegalArgumentException`**, so alias every selected column (`AS Chunk__c`) and read by that alias.
- Text can come back HTML-escaped (`&#124;` instead of `|`). Run `unescapeHtml4()` on text you put into a prompt.

## Escaping user input

The search text is an SQL string literal inside `hybrid_search(...)`. Treat it as untrusted:

```apex
private static String toSqlLiteral(String value) {
    return '\'' + value.replace('\'', '\'\'') + '\'';
}
// Also: strip control characters, normalizeSpace(), and cap the length (for example 500).
```

The prefilter argument and the relevance JSON are string literals too, so pass them through the same helper.
Never concatenate user text into DMO names or `WHERE` clauses.

## Apex as a Prompt Builder data provider (Flex templates)

Use this to replace the standard retriever with your own SQL (dedup, filters, URL and title per excerpt):

```apex
public with sharing class MySearchRetriever {
    @InvocableMethod(label='My Search Retriever')       // NO CapabilityType: "FlexTemplate://" is retired
    public static List<Response> getPrompt(List<Request> requests) { ... }

    public class Request {
        @InvocableVariable(required=true) public String query;   // name must equal the template input apiName
    }
    public class Response {
        @InvocableVariable public String Prompt;                 // exactly one member, named Prompt
    }
}
```

- Prompt Builder sends **one** request; only `requests[0]` has data. Run one query; don't loop.
- **Changing the Request fields later breaks the template** (known issue), so settle the shape first.
- Template side: the `content` uses `{!$Apex:MySearchRetriever.Prompt}`, and `templateDataProviders` contains
  `apex://MySearchRetriever`, the reference `Apex:MySearchRetriever`, and one parameter
  (`query`, `primitive://String`, `{!$Input:query}`).
- Return a fixed "no relevant content found" string on empty results **and** on exceptions, so the prompt's
  "say you don't know" rule applies instead of an action error. Log the exception.
- **Running user:** in an Agentforce chat, the class runs as the **agent user**, not you. That user needs Apex
  class access (a permission set) and Data 360 query access. Because the class swallows errors, a missing
  permission shows up as "no information" on every answer. Preview and anonymous Apex run as you and won't
  catch it.

### Shipping a new template version through metadata

Published versions can't be edited. To ship:
1. Add a new `templateVersions` block with `status` Draft and no `versionIdentifier`, then deploy.
2. Retrieve the template to read the generated id (`…=_N`).
3. Set that version to `Published`, set `activeVersionIdentifier` to it, and deploy again.

To roll back, point `activeVersionIdentifier` at the previous version.

## Testing with `sfsqlquery.SqlTester`

```apex
sfsqlquery.SqlTester.clearMocks();
ConnectApi.QuerySqlMetadataItem col = new ConnectApi.QuerySqlMetadataItem();
col.name = 'Chunk__c';
col.type = ConnectApi.TypeEnum.Varchar;               // the docs' example uses DECIMAL, which doesn't exist; use Numeric
sfsqlquery.SqlTester.setMockMetadata(new List<ConnectApi.QuerySqlMetadataItem>{ col });
ConnectApi.QuerySqlRow mockRow = new ConnectApi.QuerySqlRow();
mockRow.row = new List<Object>{ 'passage text' };     // field is `row`; the docs' `rowData` doesn't compile
sfsqlquery.SqlTester.setMockRows(new List<ConnectApi.QuerySqlRow>{ mockRow });
```

- Every query in the test returns the mock, whatever its SQL. Test the SQL builder separately (expose it with
  `@TestVisible`) and assert on the escaping and the filters.
- `ConnectApi.TypeEnum` values in this org: `ArrayOfX, BigInt, Bool, Char, Date, Double, Float, Float4, Float8,
  Integer, Interval, Json, Numeric, Oid, SmallInt, Time, Timestamp, TimestampTZ, Unspecified, Varchar`. Use
  `Numeric` for scores.
- `ConnectApi.QuerySqlRow` **can't be constructed outside a test** (it throws `UnsupportedOperationException`
  in anonymous Apex).
- To test the error path, mock metadata that lacks the columns your code reads. The accessor throws, and you
  assert on the fallback text.
