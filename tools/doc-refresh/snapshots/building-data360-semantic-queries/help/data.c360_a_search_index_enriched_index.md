# Enriched Indexing of Content Chunks | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_enriched_index.htm&type=5

DATA 360
Enriched Indexing of Content Chunks

When you create a vector or hybrid search index from unstructured data in Data 360, you can enrich the generated content chunks by extracting metadata from the content. Extracted metadata includes keywords, entities, topic overviews, questions answered by the content, and content summaries.

Chunk enrichment greatly improves retrieval accuracy, especially in cases in which you can’t use prepend fields (for example, in a UDMO path) and in question and answer agent actions. Enriched content chunks provide an alternative to intensive content curation because LLM-generated content helps improve the identification of the right chunks.

To use enriched content chunks, first create a search index and enable enriched content chunks. In AI Models, create a new custom retriever. When prompted for the search index, select a search index that was created using the enrich chunks option.

To get the most value from an enriched index, access it through a retriever. To use the metadata chunks, a retriever applies extra logic, such as reranking and intent alignment. Calling the index directly through search APIs bypasses the retriever and results in retrieval behavior closer to standard vector or hybrid search. Although introducing a retriever sometimes adds latency, it enables higher retrieval accuracy by improving how queries map to relevant, answer-ready content.

NOTE

Use of this feature in Data Cloud consumes Data 360Credits. For more information see, Billing Considerations for Unstructured Data and Search Index. Contact your account executive for more information.

Contents of Enriched Chunks

When you enable enriched content on a vector or hybrid search index, Data 360 generates three chunks: one chunk that contains the original chunk text, one chunk that contains metadata text, and one chunk that contains questions that the chunk can answer. Retrievers access these chunks to use in RAG and AI agent workflows.

NOTE Generated metadata doesn’t include personal identifying information (PII).
CHUNK TYPE METADATA TYPE DESCRIPTION
METADATA Keywords

Extracts keywords that uniquely identify the content.

Entities

Identifies and lists verbatim any of the following:

Locations
Organizations
Dates
Time
Currencies
Amounts
Percent
Products
Platforms mentioned

Topics

Extracts main topics discussed in the chunk. Includes important entities and keywords in the topic names.

Title

Generates a concise and informative title summarizing the content.

Summary Provides a summary of the content, highlighting key topics and entities. If possible, aim to encompass a minimum of 100 words and a maximum of 250 words.
QUESTION Questions If applicable, compiles a comprehensive set of detailed questions that the content in the text chunk can answer.
Data Processing for Enriched Indexing

Enriched indexes are supported in all regions where Data 360 is available. Data for enriched indexes is processed through Amazon Bedrock managed services in these regions.

us-west-2: US West (Oregon)
us-east-1: US East (Virginia)
eu-central-1: Europe (Frankfurt)
eu-central-2 Europe (Zurich)
eu-west-3: Europe (Paris)

Enable Amazon Bedrock Models (Amazon and Anthropic) in Einstein Setup to use enriched indexing. For more information, see Amazon Bedrock documentation.

Retrieval Response with Enriched Search Index
Enriched indexing enhances retrieval response by matching a question to a passage with the best possible answer in your knowledge base. While Data 360 hybrid search combines the strengths of sematically aware vector search with the precision and speed of keyword search, enriched indexing closes the gap further by finding the chunks closest to the users' question.
SEE ALSO
Create a Hybrid Search Index with Advanced Setup
Create a Vector Search Index with Advanced Setup
Billing Considerations for Unstructured Data and Search Index
Agentforce Data Library
Data Cloud Limits and Guidelines
