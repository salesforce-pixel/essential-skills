# Chunking Strategies | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_supported_chunking_strategies.htm&type=5

DATA 360
Chunking Strategies

Data 360 supports several chunking strategies and automatically selects one based on the content type. When selecting a strategy, consider which fields provide relevant context, how to divide that content, and how your generative AI, automation, or analytics application will use the retrieved results.

For example, you can use semantic-based passage extraction on the custom text fields of a Knowledge Article DMO. This strategy creates passages that can help return semantically similar results when users search Knowledge objects. Available strategies include:

Section-Aware Chunking
Semantic-based passage extraction
Conversation-based chunking
Prepend field chunking
Code Extension
Section-Aware Chunking

Section-aware chunking uses titles and headings to divide documents into sections. Text under a title or heading is chunked together until Data 360 encounters another title or heading. This keeps chunks aligned with the document structure.

When a section is too large for one chunk, Data 360 can create multiple chunks while respecting paragraph boundaries, preserving readability and context. Short paragraphs or list items can sometimes be identified as standalone sections, resulting in overly small chunks. To manage chunk size, configure these settings when you create a search index.

Max Tokens: Combine adjacent small sections into a larger chunk, optimizing chunk size while preserving coherence. See How the Max Token Setting Affects Chunking.
Overlap Tokens: When a section produces multiple chunks, specifies how many tokens to repeat from the end of one chunk at the beginning of the next. Overlap preserves the context between chunks and can improve search and retrieval.

Data 360 can group multiple paragraphs into a single chunk if their combined content stays within the configured token limit. When the limit is reached, it extends the chunk to the end of the paragraph, rather than splitting a sentence or paragraph.

For example, this document is divided into sections based on its title and following headings.

A document annotated to show section-aware chunking.

An example of the resulting chunk data model object contains these records:

CHUNK SEQUENCE NUMBER CHUNK CHUNK DATASOURCE OBJECT DATASOURCE
1 Retrievers A retriever returns relevant data from the vector database to augment a prompt. By augmenting prompts with accurate, current, and pertinent information, retrievers improve the value and relevance of LLM responses for users. . . DataSourceObject__c DataSource__c
2 Default and Custom Retrievers When a search index is created in Data Cloud, a default retriever is created automatically. You can't customize a default retriever. However, in AI Models, you can create and customize retrievers for search indexes. DataSourceObject__c DataSource__c
3 Dynamic Retrievers Some standard templates contain dynamic retrievers. A dynamic retriever is a placeholder for a retriever specified at runtime depending on the needs of the prompt template. To test a dynamic retriever, enter the retriever’s API name, which you can find in AI Models. DataSourceObject__c DataSource__c

In the Data 360 advanced search index builder, section-aware chunking is the default strategy for HTML and PDF files. For HTML documents, Data 360 strips HTML tags from the chunk text.

Semantic-Based Passage Extraction

Semantic-based passage extraction uses the meaning and structure indicated by HTML elements to divide a document into passages. These elements are treated as logical chunk boundaries.

Heading levels: 1-6 (<h1-h6>): Define headings.
Thematic break: (<hr>): Defines a thematic break.
Bold (<b>): Used when the tagged text is on its own line, or when it appears in a paragraph with font_weight set to 700 or higher, or to bold.
Strong(<strong>): Used when the tagged text is on its own line, or when it appears in a paragraph with font_weight set to 700 or higher, or to bold.
Paragraph (<p>): Used when the tagged text is on its own line.
Line break (<br>): Used when the current chunk exceeds the token limit.
NOTE When you use the passage extraction strategy for HTML documents, HTML tags are automatically stripped from before chunking. This is the default setting in the search index builder, but you can turn off it if needed.

For example, this text includes several HTML elements.

Here’s its HTML equivalent:

<h1>Enable Custom Time Zones</h1>
<p>Time zone support lets you view time-specific data...</p>

<h4>REQUIRED EDITIONS</h4>
<p>Available in Salesforce Classic and Lightning Experience</p>
<p>...</p>

<h2>Enable Time Zone Support</h2>
<ul>...</ul>

An example of the resulting chunk data model object contains these records:

CHUNKSEQUENCENUMBER CHUNK DATASOURCE OBJECT DATASOURCE
1 Enable Custom Time Zones Time zone support lets you view time-specific data.... DataSourceObject__c DataSource__c
2 REQUIRED EDITIONS Available in Salesforce Classic... DataSourceObject__c DataSource__c
3 Enable Time Zone Support From Setup, enter Analytics... DataSourceObject__c DataSource__c
4 Sync Connected Objects and Refresh Datasets Run a full Data Sync of your connected objects... DataSourceObject__c DataSource__c

If there’s no content between two heading tags, Data 360 can combine the headings and their following content into one chunk, as long as they fit within the chunk's token limit.

By default, Data 360 uses semantic-based passage extraction. If a resulting passages is too long, it processes the passage further by using window-based passage extraction. Window-based extraction uses block-level elements, such as <div> and <p>, or raw text separated by line breaks <br>, to divide documents into passages. If a paragraph doesn’t contain HTML, Data 360 aggregates the text at the sentence level.

When you use passage extraction for HTML documents, Data 360 automatically strips HTML tags from the content. This is the default in the search index builder, but you can turn off it.

Conversation-Based Chunking

Use conversation-based chunking to retrieve information from conversation transcripts, audio, and video files.

Conversation Transcripts

For transcripts, conversation-based chunking groups messages by conversation, orders them by timestamp, and packs them into chunks. Retrieval returns the conversation context rather than individual messages. If a conversation exceeds the configured limits, Data 360 splits it across multiple chunks.

Upload conversation transcripts as CSV files into a data model objects (DMOs), then select conversation-based chunking when you build a search index. This strategy isn't available for unstructured data model objects (UDMOs).

Configure a chunk with these parameters:

Chunk Field: The record field that contains the conversation text.
Group By Field: The field is used to group records into a conversation, such as a conversation ID.
Order By Field: The field used to order records chronologically, such as a timestamp for speaker turns.
Max Tokens: The maximum chunk size in tokens.
Overlap Turns: The number of final turns repeated in the next chunk to preserve continuation and context. This only applies when a conversation is split across multiple chunks.
Max Turns: The maximum number of turns or messages in a chunk.
Prepend fields to each chunk: Optionally, prepend metadata such as meeting title, or date.
Speaker Field: Currently unused.

Max Tokens and Max Turns work together. A new chunk starts when a conversation exceeds either limit. Chunks contain complete messages unless a single message exceeds Max Tokens.

Audio and Video Files

During transcription, if multiple speakers are detected, each chunk contains speech from an individual speaker.

Here are the first few lines of a transcript.

"Hello? Hi Alex, it's Sam from Bullseye. I didn't hear from you yesterday, so I wanted to check in. Hi Sam, sorry about that."

An example of the resulting chunk data model object contains these records:

CHUNKSEQUENCENUMBER CHUNK START TIMESTAMP END TIMESTAMP SPEAKER
1 Hello? 1.051 1.253 SPEAKER_00
2 Hi Alex, it 's Sam from Bullseye. I didn't hear from you yesterday, so I wanted to check in. 3.203 8.418 SPEAKER_01
3 Hi Sam, sorry about that. 10.263 11.546 SPEAKER_00
Prepend Field Chunking

Prepend fields to chunks generated from DMOs or UDMOs when you need to add metadata for context. For example, the Description field in a Knowledge article might exceed the optimal chunk size for prompt-based retrieval. Prepending the Title field to each chunk can provide more useful context in the prompt results.

Examples of useful metadata fields:

TYPE METADATA FIELD EXAMPLES
DMO (Knowledge Articles)
Title
Product Name

UDMO (External blob store connectors) File Path
UDMO (Web crawler or Sitemap connectors)
Labels
Title
URL

Configure fields to prepend in the advanced setup for vector or hybrid search indexes.

If a record’s prepended value reaches the maximum token limit, Data 360 doesn’t create chunks for that record, and the record doesn’t appear in search results. Select fields that fit within the chunk size limit.

Code Extension

Use a custom chunking function when built-in chunking strategies don't meet your content or retrieval requirements. Custom functions can apply domain-specific logic, such as preserving related sections from complex PDFs or by using prompt-driven chunking through LLM gateway calls.

To use a custom function, deploy it and select it as the chunking strategy in the search index advanced setup. For the end-to-end workflow to author, validate, deploy, and use a custom chunking function, see Use Custom Functions in Data 360.

SEE ALSO
Salesforce Help: Create Vector Search Index Configurations
Salesforce Developer: Code Extension in Data 360
Salesforce Help: Govern Content for AI Consumption
