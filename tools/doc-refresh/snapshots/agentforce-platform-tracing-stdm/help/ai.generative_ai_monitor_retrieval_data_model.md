# Data Model for Knowledge/RAG Quality Data and Metrics | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=ai.generative_ai_monitor_retrieval_data_model.htm&type=5

QUICKSTART YOUR EINSTEIN GENERATIVE AI SOLUTION
Data Model for Knowledge/RAG Quality Data and Metrics

Use the data in these DLOs/DMOs to build reports, dashboards, and queries that provide insights into knowledge retrieval events.

REQUIRED EDITIONS
Available in: Lightning Experience
Available in: Enterprise, Performance, Unlimited, and Developer Editions. Required add-on licenses vary by agent type.
About the Knowledge/RAG Quality Data and Metrics Data Model

The data model for Knowledge/RAG Quality Data and Metrics is a collection of DLOs (Data Lake Objects) and DMOs (Data Model Objects) that contain quality data and metrics.

Knowledge/RAG Quality Data and Metrics ERD

DLO/DMO DESCRIPTION
AIRetrieverRequest Represents a request to the retriever.
AIRetrieverResponse Represents a response from the retriever.
AIRetrieverQualityMetric Represents the quality scores derived by comparing the request and response.

Data is streamed to DLOs in Data 360 and then mapped to the applicable DMOs.

Prefix for Field API Names

In the default dataspace, the prefix for Field API Names is ssot__, such as ssot__Id__c. If your Salesforce org uses a custom dataspace, replace ssot__ with your dataspace's prefix, such as std__.

AIRetrieverRequest DLO

A Data 360 DLO that captures retriever request details. The AIRetrieverRequest object has these attributes.

FIELD LABEL FIELD API NAME DATA TYPE DESCRIPTION
AI Retriever Request Id Id Text Primary key. Unique identifier of the AI retriever request.
Created By CreatedById Text - Reference - Id (lookup) User who created thise record.
Created Date CreatedDate Date - Time Timestamp (date/time) when this record was created.
External Record Id ExternalRecordId Text Corresponding record Id from an external data source system.
External Source Id ExternalSourceId Text Id of an external data source system.
Feature FeatureText Text Label of the feature involved in the event origin. Identifies, in the logs, which capability or functionality triggered the retriever call or is being tracked. Examples: DocumentRetrieval, KnowledgeSearch
Last Modified By LastModifiedById Text - Reference - Id (lookup) User who most recently changed this record.
Last Modified Date LastModifiedDate Date - Time Timestamp (date/time) when a user most recently changed this record.
Query QueryText Text User query sent to the retriever.
Request Information RequestInfoText Text Additional information in the request (key-value pairs in JSON format).
Request Timestamp RequestTimestamp Date - Time Timestamp (date/time) when the retriever request occurred.
Retriever API Name RetrieverApiName Text API name of the retriever associated with this request
Retriever ReferenceId RequestReferenceId Text Reference Id of the calling component, service, or process that sent the request to the retriever to fetch relevant information. Examples: agent, prompt, or Apex class.
SessionId SessionId Text Session id of the agent that called the retriever.
Source Additional Information SourceAdditionalInfoTxt Text Additional information associated with the source asset that originated this call (key-value pairs in JSON format). Example: PROMPT
Source Asset API Name SourceAssetApiName Text API name of the source asset that originated this call. Example: PROMPT
Source Asset Type SourceAssetTypeName Text Type of the source asset that originated this call. Example: PROMPT
Source Asset Version SourceAssetVersion Text Version of the source asset that originated this call. Example: PROMPT
SpanId SpanId Text Span id is generated from the component that called the retriever directly.
System Modified Stamp SystemModstamp Date - Time Timestamp (date/time) when this record was last modified by a user or an automated process.
TraceId TraceId Text Trace id of the agent session in which this retriever call occurred.
AIRetrieverResponse DLO

A Data 360 DLO that captures retriever response details. The AIRetrieverResponse object has these attributes.

FIELD LABEL FIELD API NAME DATA TYPE DESCRIPTION
AI Retriever Response Id Id Text - Primary Key Primary key. Unique identifier of the AI retriever response.
AI Retriever Request AiRetrieverRequestId Text - Reference - Id (parent) Foreign key reference to AIRetrieverRequestId that corresponds to this retriever response.
Created By CreatedById Text - Reference - Id (lookup) User who created this record.
Created Date CreatedDate Date - Time Timestamp (date/time) when this record was created.
External Record Id ExternalRecordId Text Corresponding record Id from an external data source system.
External Source Id ExternalSourceId Text Id of an external data source system.
Last Modified By LastModifiedById Text - Reference - Id (lookup) User who most recently changed this record.
Last Modified Date LastModifiedDate Date - Time Timestamp (date/time) when a user most recently modified this record.
Response Information xResponseInfoText Text Additional information in the response (key/value pairs in JSON format).
Response Timestamp ResponseTimestamp Date - Time Timestamp (date/time) when this response was emitted.
Result ResultText Text JSON representation of the retriever response, including chunk, SourceRecordId, and so on.
Sort Index SortIndexNumber Number - Integer SortIndex of the chunks that the retriever returned.
Source Record SourceRecordId Text Document reference linked to the chunk.
System Modified Stamp SystemModstamp Date - Time Timestamp (date/time) when this record was most recently modified by a user or an automated process.
AIRetrieverQualityMetric DMO

A Data 360 DMO that captures retriever quality metrics details. It’s used as the basis for reports, dashboards, and queries. The AIRetrieverQualityMetric object has these attributes.

FIELD LABEL FIELD API NAME DATA TYPE DESCRIPTION
AI Retriever Quality Metric Id Id__c Text Primary key. Unique identifier associated with this metric result.
Agent Generated Response AgentGeneratedResponseText__c Text Context extracted from the ResponseText in AI Response Generation.
AI Gateway Request CustomDMORef_AiGatewayRequestId__c Text - Reference - Id (lookup) Foreign key reference to the GenAIGatewayRequestId associated with this metric result.
AI Gateway Request Id AiGatewayRequestId__c Text Reference to the GenAIGatewayRequestId associated with this metric result.
AI Response Generation CustomDMORef_AiResponseGenerationId__c Text Foreign key reference to AIResponseGeneration (Custom DMO GenAIGeneration) associated with this metric result.
AI Response Generation Id AiResponseGenerationId__c Text Reference to AIResponseGeneration associated with this metric result.
AI Retriever Request CustomDMORef_AiRetrieverRequestId__c Text Foreign key reference to AIRetrieverRequestId associated with this metric result
AI Retriever Request Id AI Retriever Request Id__c Text Reference to AIRetrieverRequestId associated with this metric result.
Answer Relevancy Score AnswerRelevancyScoreNumber__c Number - Decimal Answer Relevancy Score. How completely and how well is the question answered?
Context Precision Score ContextPrecisionScoreNumber__c Number - Decimal Context Precision Score. What proportion of the right knowledge was found?
Created By CreatedById__c Text - Reference - Id (lookup) User who created the record.
Created Date CreatedDate__c Date - Time Timestamp (date/time) when this record was created.
External Record Id ExternalRecordId__c Text Corresponding record Id from an external data source system.
External Source Id ExternalSourceId__c Text Id of an external data source system.
Faithfulness Relevancy Score FaithfulnessRelevancyScoreNumber__c Number - Decimal Faithfulness Relevancy Score. How well did the Agent use the found knowledge?
Last Modified By LastModifiedById__c Text - Reference - Id (lookup) User who most recently changed this record.
Last Modified Date LastModifiedDate__c Date - Time Timestamp (date/time) when a user most recently changed this record.
Last Processed Request Timestamp LastProcessedReqTimestamp__c Date - Time Timestamp (date/time) of the AIRetrieverRequest that was last processed for metric evaluation.
Metric Created Timestamp MetricCreatedTimestamp__c Date - Time Timestamp (date/time) when the metric result was generated.
Retrieved Context Id List RetrievedContextIdListText__c Text List of context Ids (Top-K) extracted from ResultText in the retriever response. Used for reporting.
Retriever Api Name RetrieverApiName__c Text API name of the retriever associated with this request.
Retriever Trace Id RetrieverTraceId__c Text Trace Id (for example, from OTel) that was generated during the retriever request.
Retriever Trace Span Id RetrieverTraceSpanId__c Text Trace Span Id (for example, from OTel) that was generated during the retriever request. Reference to Telemetry Trace DMO.
Source Document Id List SourceDocumentIdListText__c Text List of Source Record Ids from the retriever response. Used for reporting.
System Modified Stamp SystemModstamp__c Date - Time Timestamp (date/time) when this record was last modified by a user or an automated process.
UserUtterance UserUtteranceText__c Text Context extracted from the user utterance in the retriever request. Used for reporting.
