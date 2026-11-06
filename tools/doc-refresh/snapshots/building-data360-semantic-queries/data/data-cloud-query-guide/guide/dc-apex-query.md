# Query Data 360 Data with Apex

Use Apex to query Data 360 data directly from your Salesforce org. Access unified customer insights and act on them immediately within your Salesforce automations.

## sfsqlquery Namespace

Use the `sfsqlquery` namespace when you need an easy and intuitive way to execute queries with iterators and typed row accessors.

**When to use:** Run SQL queries on Data 360

- Synchronous iteration over query results
- Typed column value accessors (getString, getInteger, etc.)
- Asynchronous processing of large datasets with SqlQueueable
- Resume queries from saved query IDs

**Common workflows:**

The namespace provides five classes that support three primary workflows:

1. **Execute a new query synchronously:**\
   SqlStatement → SqlRowIterator → Row

2. **Fetch results of a previously executed query:**\
   QueryHandle → SqlRowIterator → Row

3. **Process large datasets asynchronously:**\
   SqlQueueable → SqlRowIterator → Row

See [sfsqlquery Namespace](https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_namespace_sfsqlquery.htm) in the Apex Reference.

## Authentication and Permissions

Apex methods use the current user's session context and permissions automatically. Ensure users have appropriate Data 360 permissions assigned through permission sets or profiles.

See [Getting Started with Apex](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_intro_get_started.htm) in the Apex Developer Guide.

## Best Practices

- **Use asynchronous patterns**: For long-running queries, implement polling logic to avoid governor limits
- **Handle errors**: Check query status for failures and implement retry logic
- **Test with smaller datasets**: Validate your query logic with `LIMIT` clauses before processing full datasets

## Examples

### Execute a Query Synchronously

Build a query with SqlStatement, execute it synchronously with SqlRowIterator, and access typed column values using the Row class. The SqlStatement.create() method builds the query, the execute() method runs it synchronously, and Row provides typed accessor methods like getString() to retrieve column values.

```apex
sfsqlquery.SqlStatement stmt = sfsqlquery.SqlStatement.create(
    'SELECT ssot__FirstName__c, ssot__LastName__c FROM ssot__Individual__dlm LIMIT 10', 
    'default'
).withWorkloadName('my_workload');

sfsqlquery.SqlRowIterator iterator = stmt.execute();

for (sfsqlquery.Row row : iterator) {
    String firstName = row.getString('ssot__FirstName__c');
    String lastName = row.getString('ssot__LastName__c');
    System.debug(firstName + ' ' + lastName);
}
```

### Resume a Previously Executed Query

Resume a query from a saved query ID using QueryHandle. The QueryHandle.create() method takes a saved query ID and uses withOffset() to skip already-processed results. This is useful when you need to retrieve additional results from a previously executed query.

```apex
String savedQueryId = iterator.getQueryId();
sfsqlquery.QueryHandle handle = sfsqlquery.QueryHandle.create(savedQueryId, 'default')
    .withOffset(10);
sfsqlquery.SqlRowIterator resumedIterator = new sfsqlquery.SqlRowIterator(handle);
```

### Process Large Datasets Asynchronously

Process large datasets asynchronously using SqlQueueable. The custom class extends SqlQueueable and implements two key methods: processDataChunk() to handle each page of results, and chainNextJob() to automatically continue processing subsequent pages. This pattern prevents governor limit issues when working with large result sets.

```apex
public class MyQueryJob extends sfsqlquery.SqlQueueable {
    public MyQueryJob(sfsqlquery.SqlStatement stmt) { super(stmt); }
    public MyQueryJob(sfsqlquery.QueryHandle handle) { super(handle); }

    public override void processDataChunk() {
        for (sfsqlquery.Row row : getRows()) {
            System.debug(row.getString('ssot__FirstName__c'));
        }
    }

    public override void chainNextJob(sfsqlquery.QueryHandle handle) {
        System.enqueueJob(new MyQueryJob(handle));
    }
}

sfsqlquery.SqlStatement stmt = sfsqlquery.SqlStatement.create(
    'SELECT ssot__FirstName__c FROM ssot__Individual__dlm', 'default'
);
System.enqueueJob(new MyQueryJob(stmt));
```

## Low-Level Interface

For backward compatibility, the `ConnectApi.CdpQuery` class remains available as a low-level interface that directly mirrors the Connect REST API. We recommend using the `sfsqlquery` namespace for all new development.

See [ConnectApi.CdpQuery Methods](https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_ConnectAPI_CdpQuery_static_methods.htm) in the Apex Reference.

## See Also

- [Query Data 360 Data using Query API](https://developer.salesforce.com/docs/data/data-cloud-query-guide/references/data-cloud-query-api-reference/c360a-api-queryservices-overview.md) - Complete API reference
- [Data 360 SQL Query APIs](/docs/data/data-cloud-query-guide/guide/dc-sql-query-apis.md) - Overview of query API options
- [Get Started With Data 360 SQL](/docs/data/data-cloud-query-guide/guide/dc-query-section.md) - SQL syntax and examples
