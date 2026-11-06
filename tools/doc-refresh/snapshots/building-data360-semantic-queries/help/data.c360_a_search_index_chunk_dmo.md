# Chunk DMO | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_chunk_dmo.htm&type=5

DATA 360
Chunk DMO

The chunk data model object (CDMO) stores chunked content for each field from a chunked object.

The chunk DMO had these attributes.

FIELD LABEL FIELD API NAME DATA TYPE DESCRIPTION
Chunk Chunk__c Text The generated chunk
Chunk Sequence Number ChunkSequenceNumber__c Number Sequential number in which the chunk was generated from the source data; sequence starts at 0
Citation Citation__c Text Citation that references the source data from which the chunk was created.
Data Source DataSource__c Text API name of the field from the DMO/UDMO that contains content for the generated chunk. This is a default pre-filtering field.
Data Source Object DataSourceObject__c Text API name of the DMO/UDMO that contains content for the generated chunk
Internal Organization InternalOrginzation__c Text Unused
Key Qualifier Record Id KQ_RecordId__c Text Key qualifier field for Record ID
Key Qualifier Source Record Id KQ_SourceRecordId__c Text Key qualifier field for Source Record ID
Record Id RecordId__c Text Primary key: Unique identifier of each chunk record
Secondary Source Record Id SecondarySourceRecordId__c Text Primary ID of the source record in attachment UDMO from which the chunk was generated. Populated only when the search index includes file attachments and only for chunks that are generated from a file attachment.
Source Record Id SourceRecordId__c Same as Primary ID of source record Primary ID of the source record of the DMO/UDMO from which the chunk was generated
