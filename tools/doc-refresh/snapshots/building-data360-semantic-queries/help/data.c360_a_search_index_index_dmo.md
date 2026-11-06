# Index DMO | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_index_dmo.htm&type=5

DATA 360
Index DMO

The index data model object (IDMO) stores generated vector embeddings.

The Index DMO has these attributes.

FIELD LABEL FIELD API NAME DATA TYPE DESCRIPTION
Data Source DataSource__c Text API name of the field from the DMO/UDMO that contains content for the generated chunk. This is a default pre-filtering field.
Data Source Object DataSourceObject__c Text A field populated with the internal filename that contains the chunk for which the vector embedding was generated
Internal Organization InternalOrganization__c Text Unused
Key Qualifier Record Id KQ_RecordId__c Text Key qualifier field for Record ID
Record Id RecordId__c Text Primary key: Unique identifier of each vector embedding
Source Record Id SourceRecordId__c Same as Primary ID of source record Primary ID of the generated chunk table. This matches the chunk table's RecordId__c.
Vector Embedding VectorEmbedding__c Array of floats Generated vector embedding
