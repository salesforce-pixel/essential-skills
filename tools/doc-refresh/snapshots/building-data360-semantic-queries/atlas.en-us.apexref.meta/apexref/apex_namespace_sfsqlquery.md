# sfsqlquery Namespace

Source: https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_namespace_sfsqlquery.htm

sfsqlquery Namespace
 
 Contains classes for executing SQL queries against Data 360 data spaces from Apex.

 
 The following are the classes in the sfsqlquery namespace.

 
 
 
 QueryHandle Class 

Tracks the runtime execution state of a Data 360 SQL query as it progresses through submission, execution, and result retrieval. Use QueryHandle to resume a previously submitted query from a saved query ID in a new SqlRowIterator or a new SqlQueueable job.

 
 Row Class 

Wraps a single Data 360 SQL query result row and provides typed accessor methods for retrieving column values by name or by 0-based index. Row instances are produced by SqlRowIterator and SqlQueueable ; you don't construct Row objects directly during normal usage.

 
 SqlQueueable Class 

Abstract base class for executing long-running Data 360 SQL queries asynchronously in chained Queueable jobs. Implements Queueable and Database.AllowsCallouts . Create a concrete subclass that implements processDataChunk() to process each page of results and chainNextJob() to enqueue the next job when more data remains.

 
 SqlRowIterator Class 

Synchronous iterator for executing Data 360 SQL queries and retrieving results row-by-row within the current transaction. Implements Iterator<Row> and Iterable<Row> for use in both for-each and while loops. The iterator is single-use; once all rows are consumed, iterating again does not restart from the beginning.

 
 SqlStatement Class 

Encapsulates the inputs required to execute a Data 360 SQL query against a data space. Build a statement from a raw SQL string or a pre-built ConnectApi.QuerySqlInput object, and then execute synchronously with SqlRowIterator or pass it to a SqlQueueable subclass for asynchronous processing.

 
 SqlTester Class 

Test utility for mocking Data 360 SQL query API responses in Apex tests. The framework automatically detects the test context via Test.isRunningTest() and returns mocked responses when configured. Call clearMocks() before each test to ensure a clean state.
