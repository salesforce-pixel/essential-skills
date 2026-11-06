# How the Max Token Setting Affects Chunking | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_max_token_setting.htm&type=5

DATA 360
How the Max Token Setting Affects Chunking

When you set the chunking strategy in a search index configuration, you set the max token limit to control how much text is included in a chunk. In Data 360, the max token limit is set to 512 by default.

Embedding models create tokens from text and they ignore any text beyond their max token limit. However the concept of "token" differs by language as well as by embedding model, so it is not reliable to count chunks directly from text.

When you create a search index, token creation works as follows: Data 360 separates sentences in your content and then merges the sentences into chunks based on your specified max token setting. Finally, the embedding algorithm converts each chunk into a vector.

To approximate the token count when merging sentences into chunks, Data 360 uses the number of words for Latin-based languages and the number of punctuation marks for non-Latin-based languages (such as Japanese). In Latin-based languages, a word is approximately one token, but in non-Latin-based languages, the relationship between characters and tokens isn’t as clear. With that in mind, a Latin-based language chunk of 512 words is typically within the 512 token limit. For non-Latin-based languages, however, 512 punctuation marks can exceed 512 tokens due to how the embedding algorithm works. In such cases, not all text that is included in the chunk gets included in the embedding, which can impact the relevance of your search results. For this type of content, use a max token limit lower than 512.
