# Hybrid Search Autodrop Best Practices | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=data.c360_a_hybridsearch_autodrop_best_practices.htm&type=5

DATA 360
Hybrid Search Autodrop Best Practices

Use these best practices to configure autodrop for Data 360hybrid search results.

Use these recommended values for autodrop, for keyword search results use 2 and for vector search results use 5. Test these configurations and adjust them as needed for your use case and queries.
For keyword search results we recommend autodrop value of 2 and for vector search results we recommend a autodrop value of 5.
{ "autodrop_keyword": {"num_drops": 2}, "autodrop_vector":{"num_drops": 5 }}
The default autodrop value is less aggressive for keyword search results.
{ "autodrop_keyword": {"num_drops": 5}, "autodrop_vector":{"num_drops": 5 }}
Due to the nature of hybrid search results distribution autodrop can lead to unexpected behavior. We recommend that you use the “autodrop_vector” and “autodrop_keyword” parameters instead of the “autodrop_hybrid” parameter.
select * from hybrid_search(
table(<Search_index_DMO>),
‘<Search String>’,
'<PreFilteringColumn><Operator><Value>',
'<Limit Results>',
‘{ "autodrop_keyword": {"num_drops": 2}, "autodrop_vector":{"num_drops": 5 }}’
);

To ensure your search results include the most relevant results, calibrate the number of autodrops with a set of test queries and gradually vary the value until the relevant results are present in the result set.

To make hybrid search autodrop less aggressive and retain more results, consider increasing the num_drops value. An overly aggressive autodrop can cut off important documents, especially if score drops aren't pronounced in your data set or if you have a broader definition of relevant results. You can adjust “autodrop_keyword”, “autodrop_vector”, or “autodrop_hybrid” based on where you notice a loss of relevant results.

To make hybrid search autodrop more aggressive and retain the most highly relevant results, decrease the value of num_drops. For instance, if your search results still include a significant number of irrelevant documents even after the initial autodrop, and the default num_drops doesn’t’ effectively filter out the noise, you should decrease the num_drops value.

If the value of autodrop exceeds the actual number of score drops in the list, no truncation is applied.
If documents contain many similar terms, applying autodrop on keyword results helps to keep only the most relevant results.
Alternatively, you can simply reduce your result set by setting a limit on the number of results returned for a query. For more details see, Run Hybrid Search Queries with Query API. In this example, the limit is set to two results for the query.
select * from hybrid_search(
table(Knowledge_full_index__dlm),
'How to input special mark/character when using keyboard input data field','', 2)
EXAMPLE This example shows a hybrid search query without autodrop configuration.
select Chunk__c, hybrid_score__c, keyword_score__c, vector_score__c, chk.SourceRecordId__c
from hybrid_search(table(Indeed_English_index__dlm), 'Maximize', '', 100, '{ "dfr" : {} }') hsearch
join Indeed_English_chunk__dlm chk on hsearch.RecordId__c = chk.RecordId__c
ORDER BY hybrid_score__c DES

With autodrop configured for vector search results and keyword search results, the search results are scoped down to the most relevant results.

select Chunk__c, hybrid_score__c, keyword_score__c, vector_score__c, chk.SourceRecordId__c
from hybrid_search(table(Indeed_English_index__dlm), 'Maximize', '', 100, '{ "autodrop_keyword": {"num_drops": 2}, "autodrop_vector":{"num_drops": 5 }}') hsearch
join Indeed_English_chunk__dlm chk on hsearch.RecordId__c = chk.RecordId__c
ORDER BY hybrid_score__c DESC
