---
name: building-data360-semantic-queries
description: "Build and debug Salesforce Data 360 (Data Cloud) semantic search SQL — vector_search() and hybrid_search() — including the index/chunk/source join chain, join-key discovery, pre-filtering, fusion ranking (RRF/LFR/DFR), and autodrop. TRIGGER when: user writes or debugs vector_search or hybrid_search SQL, builds RAG retrieval over a Data Cloud search index, asks why a search join returns zero rows, tunes search relevance or result counts, works with index/chunk DMOs (VECTOR_EMBEDDING, CONTENT categories), runs Data 360 SQL from Apex (sfsqlquery, ConnectApi.CdpQuery), or builds an Apex data provider that replaces a standard retriever in a prompt template. DO NOT TRIGGER when: creating the search index configuration itself in Setup or Connect API (that is index setup, not querying), writing plain SOQL (use querying-soql), general Data Cloud segmentation (use segmenting-datacloud), or retrieval config in Agentforce/Prompt Builder rather than raw SQL."
license: MIT
metadata:
  version: "1.5"
---

<!--
Changelog
1.5 — Imported into essential-skills (2026-11-06) from the personal
      ~/.claude/skills copy. Doc sources tracked by tools/doc-refresh.
-->

# building-data360-semantic-queries

Write working `vector_search()` / `hybrid_search()` SQL against Data 360 search indexes on the first or second attempt, instead of discovering the schema by trial and error.

The hard part is never the search function. It is the **join chain back to readable text**, whose keys vary per index and are not discoverable from the DMO metadata alone. Follow the discovery ladder below rather than guessing.

## The three-object model

Building a search index produces two new DMOs alongside your source:

```
Source DMO / UDMO  (your data; category is often DIRECTORY_TABLE for crawled files)
      │  chunking
      ▼
Chunk DMO  (CDMO, category CONTENT) ......... Chunk__c, RecordId__c, SourceRecordId__c
      │  embedding
      ▼
Index DMO  (IDMO, category VECTOR_EMBEDDING) ... VectorEmbedding__c ← pass this to TABLE()
```

The Help docs use the abbreviations CDMO and IDMO, and "Data 360" (Data Cloud was renamed on Oct 14, 2025; older docs and UI still say Data Cloud).

**You query the index DMO, but it returns only IDs and scores — never text.** Every usable query joins index → chunk (for the passage) → source (for URL/title/metadata).

Category alone does not tell you whether an index supports hybrid: hybrid indexes also produce a `VECTOR_EMBEDDING` DMO. Probe it (Rung 4).

### Documented fields, and what the IDs actually mean

**Index DMO** ([docs](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_index_dmo.htm&type=5)):

| Field | Meaning |
|---|---|
| `RecordId__c` | primary key of the **vector embedding itself** |
| `SourceRecordId__c` | **"Primary ID of the generated chunk table. This matches the chunk table's `RecordId__c`."** |
| `DataSource__c` | API name of the *field* whose content was chunked. **Default pre-filtering field.** |
| `DataSourceObject__c` | internal filename containing the chunk |
| `VectorEmbedding__c` | array of floats |
| `KQ_RecordId__c` | key qualifier for Record ID |
| `InternalOrganization__c` | unused |

**Chunk DMO** ([docs](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_chunk_dmo.htm&type=5)):

| Field | Meaning |
|---|---|
| `Chunk__c` | the passage text |
| `RecordId__c` | primary key of the chunk |
| `SourceRecordId__c` | primary ID of the **source** DMO/UDMO record |
| `ChunkSequenceNumber__c` | position in source document, **starts at 0** |
| `Citation__c` | citation referencing the source data |
| `DataSource__c` | API name of the chunked *field*. **Default pre-filtering field.** |
| `DataSourceObject__c` | API name of the source DMO/UDMO |
| `KQ_RecordId__c`, `KQ_SourceRecordId__c` | key qualifiers |

So the canonical chain, straight from the docs, is:

```
index.SourceRecordId__c  →  chunk.RecordId__c  →  (chunk.SourceRecordId__c → source PK)
```

**Use `SourceRecordId__c` as the index-side join key for both functions.**

- **`hybrid_search`:** the docs state that the output `RecordId__c` "has the same value as the
  `SourceRecordId__c` field", so either join key is correct by spec. Salesforce's own examples use both
  (`hsearch.SourceRecordId__c = chnk.RecordId__c` and `hsearch.RecordId__c = chk.RecordId__c`).
- **`vector_search` and the index DMO itself:** the two columns are semantically different (embedding
  PK vs chunk PK). They often hold identical values, so either appears to work, but only
  `SourceRecordId__c` is documented to match the chunk table. The vector-search doc examples still join
  on `v.RecordId__c = c.RecordId__c`. That works when the values coincide but isn't guaranteed.

**Instances carry undocumented extras and naming drift.** Real chunk DMOs have been seen with
`Citations__c` (plural, vs documented `Citation__c`), plus `ChunkFormat__c` (seen as `DEFAULT`),
`ChunkType__c` (seen blank), `MediaSource__c`, `SecondarySourceRecordId__c`. Index DMOs may add
`KQ_SourceRecordId__c`. Enriched indexes add more; see below. Always
read the actual DMO field list rather than assuming the documented set.

### Enriched indexes: not every chunk is passage text

If the index was built with **enriched content chunks**, Data 360 generates three chunks for each
original chunk ([docs](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_enriched_index.htm&type=5)):

- the original text
- a **METADATA** chunk (keywords, entities, topics, a generated title and a summary)
- a **QUESTION** chunk (questions the content can answer)

The docs say that calling the index directly through the search APIs "bypasses the retriever". The
retriever's reranking and intent alignment are lost, and behaviour is closer to plain vector or hybrid
search. For raw SQL, this means:

- `Chunk__c` can come back as a keyword list or a list of synthetic questions instead of passage text.
- `GROUP BY c.Chunk__c` won't merge the three variants of one passage, so a single passage can fill
  three result slots.

#### How to recognise an enriched index

On a real enriched hybrid index, the index DMO, the chunk DMO **and the `hybrid_search()` output** all
carry four extra columns: `ChunkProcessingType__c`, `SourceChunks__c`, `HierarchyLevel__c` and
`ClusterId__c` (index DMO only). An index built with enrichment off doesn't have these columns, and
selecting `ChunkProcessingType__c` fails with `unknown column`. That's a quick way to tell which kind
of index you have.

| Column | Values seen | Meaning |
|---|---|---|
| `ChunkProcessingType__c` | `PLAIN`, `QUESTION`, `METADATA` | **The discriminator.** `PLAIN` is the original passage text. |
| `SourceChunks__c` | `''` on PLAIN; one 36-char chunk `RecordId__c` on QUESTION/METADATA | Links a generated chunk to **its original PLAIN passage** |
| `HierarchyLevel__c` | NULL | Unused in the observed index |
| `ChunkType__c` | blank (`' '`) | **Not** the discriminator, despite its name |

Observed distribution on one index: 97 PLAIN, 75 METADATA, 60 QUESTION. For QUESTION and METADATA
chunks, `SourceRecordId__c` still points at the **source** record, the same as for their PLAIN
passage.

Profile it first:

```sql
SELECT ChunkProcessingType__c, COUNT(*) AS n,
       MIN(LENGTH(SourceChunks__c)) AS min_len, MAX(LENGTH(SourceChunks__c)) AS max_len
FROM <Chunk_DMO> GROUP BY ChunkProcessingType__c
```

Before relying on the mapping, verify that `SourceChunks__c` holds exactly one ID (min = max = 36)
and that no generated chunk is orphaned:

```sql
SELECT COUNT(*) AS orphans
FROM <Chunk_DMO> q LEFT JOIN <Chunk_DMO> p ON q.SourceChunks__c = p.RecordId__c
WHERE q.ChunkProcessingType__c <> 'PLAIN' AND p.RecordId__c IS NULL
```

#### Query pattern: map every hit to its original passage

Don't filter QUESTION and METADATA hits out. They're often the *best* match, because a QUESTION chunk
phrased like the user's question can rank #1. Instead, resolve each hit to its PLAIN passage
**directly from the search output** and join the chunk table once:

```sql
SELECT
  MAX(h.hybrid_score__c) AS Score__c,
  MAX(s.<Url_Field>)     AS URL__c,
  p.Chunk__c             AS Chunk__c
FROM hybrid_search(TABLE(<Index_DMO>), '<user question>', '', 30, '<autodrop JSON>') h
JOIN <Chunk_DMO> p
  ON p.RecordId__c = COALESCE(NULLIF(h.SourceChunks__c, ''), h.SourceRecordId__c)
JOIN <Source_DMO> s ON p.SourceRecordId__c = s.<Join_Key>
GROUP BY p.Chunk__c
ORDER BY MAX(h.hybrid_score__c) DESC
LIMIT 6
```

- **`NULLIF(..., '')` is required.** On PLAIN hits, `SourceChunks__c` is an empty string, not NULL, so
  a bare `COALESCE` would join on `''` and drop every PLAIN hit.
- **`GROUP BY p.Chunk__c`** merges a passage that matched directly *and* through its QUESTION or
  METADATA chunk, so it fills one slot instead of up to three.
- **`MAX(score)`** keeps the best of those matches.

The alternative, `WHERE c.ChunkProcessingType__c = 'PLAIN'`, is simpler but throws away the
enrichment's main retrieval benefit and shrinks the result set after autodrop has already cut.

If you need enrichment's full accuracy benefit (reranking and intent alignment), query through a
retriever instead of raw SQL.

## Function signatures

```sql
vector_search(TABLE(<Index_DMO>), '<query text>', '<prefilter>', <k>)
hybrid_search(TABLE(<Index_DMO>), '<query text>', '<prefilter>', <k> [, '<relevance JSON>'])
```

Positional. Empty prefilter is `''`. Only `hybrid_search` takes the 5th JSON argument.

| Function | Output columns |
|---|---|
| `vector_search` | `score__c`, `RecordId__c`, `SourceRecordId__c`, `ContextField__c`, `DataSource__c`, `VectorEmbedding__c` |
| `hybrid_search` | `vector_score__c`, `keyword_score__c`, `hybrid_score__c`, `RecordId__c`, `SourceRecordId__c`, + same context columns |

**`KQ_RecordId__c` is NOT projected** by either function, even though it exists on the index DMO. The Salesforce docs show a join predicate using it — that predicate fails with an unresolved-column error. Omit it.

## Discovery ladder

Run these in order. Each rung isolates one failure mode. Do not skip to a full query.

### Rung 1 — does the index answer at all
```sql
SELECT * FROM vector_search(TABLE(<Index_DMO>), 'a natural question', '', 5)
```
Confirms the index name and that embeddings exist. Note whether `RecordId__c` and `SourceRecordId__c` hold identical values (they often do).

### Rung 2 — get the chunk text
```sql
SELECT v.score__c AS Score__c, c.Chunk__c AS Chunk__c
FROM vector_search(TABLE(<Index_DMO>), 'a natural question', '', 5) v
JOIN <Chunk_DMO> c ON v.SourceRecordId__c = c.RecordId__c
ORDER BY v.score__c DESC
```
`SourceRecordId__c` is the documented match for `chunk.RecordId__c`. If this returns zero while Rung 1
returned rows, fall back to `v.RecordId__c = c.RecordId__c` — on indexes where the two columns hold
identical values, either works.

### Rung 3 — find the chunk→source key (the usual blocker)

Do **not** guess. Compare value shapes:

```sql
SELECT SourceRecordId__c, KQ_SourceRecordId__c, DataSourceObject__c, MediaSource__c
FROM <Chunk_DMO> LIMIT 5;

SELECT <every plausible id/path/url column> FROM <Source_DMO> LIMIT 5;
```

Then confirm with a match count across candidates:

```sql
SELECT 'CandidateA' AS Candidate, COUNT(*) AS Matches
FROM <Chunk_DMO> c JOIN <Source_DMO> s ON c.SourceRecordId__c = s.<CandidateA>
UNION ALL
SELECT 'CandidateB', COUNT(*)
FROM <Chunk_DMO> c JOIN <Source_DMO> s ON c.SourceRecordId__c = s.<CandidateB>
```

Shape heuristics for `chunk.SourceRecordId__c`:

| Value shape | Likely source column |
|---|---|
| 40-char hex | `ExternalSourceId__c` (check `Hash__c` too) |
| UUID | `ExternalSourceId__c`, `Id__c` |
| `dir/sub/file.ext` | `FilePath__c`, `ResolvedFilePath__c` |
| `https://…` | `URL__c`, `OriginalFilePath__c` |

A **non-zero but implausibly large** match count means fan-out (duplicate source rows sharing an id). Still the right key — verify by checking the final query returns ≤ k rows.

`MediaSource__c` often reads `<DLO_name>:<FilePath>` — useful evidence that FilePath is involved, but it is frequently NULL, so never join on it.

### Rung 4 — probe hybrid
Swap in `hybrid_search`, join on `h.SourceRecordId__c = c.RecordId__c`, order by `hybrid_score__c DESC`.

- Works, `keyword_score__c` non-zero → hybrid is live, prefer it
- Function/index error → index is vector-only; needs a rebuild with `searchType: HYBRID`
- Runs but `keyword_score__c` is 0 everywhere → keyword index empty or misconfigured

Test with a **literal** query (a proper noun, code, or exact phrase), not a paraphrase. Paraphrases are where vector already wins, so they show no difference.

## Production template

```sql
SELECT
  MAX(h.hybrid_score__c) AS Score__c,
  MAX(s.<Url_Field>)     AS URL__c,
  c.Chunk__c             AS Chunk__c
FROM hybrid_search(
  TABLE(<Index_DMO>),
  '<user question>',
  '',
  30,
  '{ "autodrop_keyword": {"num_drops": 2}, "autodrop_vector": {"num_drops": 5} }'
) h
JOIN <Chunk_DMO> c  ON h.SourceRecordId__c = c.RecordId__c
JOIN <Source_DMO> s ON c.SourceRecordId__c = s.<Join_Key>
GROUP BY c.Chunk__c
ORDER BY MAX(h.hybrid_score__c) DESC
LIMIT 6
```

The autodrop setting is Salesforce's documented starting point: keyword 2, vector 5. Calibrate it for
your corpus (see [Autodrop](#autodrop)). `'{ "autodrop_hybrid": {"num_drops": 3} }'` has also shipped
successfully on a real index (see `references/worked-example.md`), but Salesforce recommends against
`autodrop_hybrid`.

Design notes worth preserving when adapting it:

- **Over-fetch then collapse.** `k=30` with `LIMIT 6`. Dedup after a small k leaves 2–3 usable chunks.
- **`GROUP BY c.Chunk__c`** removes byte-identical duplicates. `MAX()` on other columns is only there to satisfy SQL's aggregate requirement.
- **`LIMIT` is a ceiling**, not the primary control — autodrop usually cuts first.

Verified available: `COALESCE`, `NULLIF`, `UNION ALL`, `GROUP BY`, `MAX`, `LIKE`, `ORDER BY <aggregate>`. Use `COALESCE(NULLIF(s.Title__c,''), s.FileName__c, s.URL__c)` when titles are sparse.

## Pre-filter vs outer WHERE

The single most consequential distinction. Get it wrong and filters silently do nothing useful.

| | Pre-filter (arg 3) | Outer `WHERE` |
|---|---|---|
| Applied | before ANN search | after retrieval |
| Fields | **only those registered at index creation** | any joined field |
| Cost | narrows candidate set, fast | needs large `k` or you filter down to nothing |

**Check what is actually prefilterable by listing the index DMO's fields.** If it only has `ContextField__c`, `DataSource__c`, `DataSourceObject__c`, `InternalOrganization__c`, the ID columns and `VectorEmbedding__c`, then no business fields were registered and prefiltering is effectively unavailable — all narrowing must go in the outer `WHERE` with a raised `k`.

**`DataSource__c` is always available as a pre-filter**, on both the index and chunk DMOs. Its value is
the **API name of the field that was chunked** — e.g. `FilePath__c`, `Content_c__c` — not a source
system name. That makes it genuinely useful when an index chunks several fields per record: it lets you
restrict retrieval to chunks derived from one field.

```sql
hybrid_search(TABLE(<Index_DMO>), 'question', 'DataSource__c=''Content_c__c''', 30)
```

Confirm the actual values first with `SELECT DISTINCT DataSource__c FROM <Chunk_DMO>` — values are
case-sensitive.

### Prefilter syntax rules

- **Quotes double** inside the SQL string: `'strField != ''v1'' and strField2 in (''a'',''b'')'`
- **Date literals differ between functions** — the one real API inconsistency:
  - `vector_search`: `'DateType=''2024-05-08'''` (quoted)
  - `hybrid_search`: `'DateType=2024-05-08'` (**unquoted**)
  - Copy-pasting a filter between them breaks silently.
  - DateTime values follow the same rule and accept a `Z` or custom offset:
    `'DateTimeTypeWithTimezone=''2024-05-08T15:28:07.000-08:30'''` (vector) and
    `'DateTimeTypeWithTimezone>=2024-05-08T15:28:07.000Z'` (hybrid).
- **Range comparisons on dates and numbers** are documented for `hybrid_search`:
  `'DateType<2024-05-08'`, `'NumField=2'`, `'NumField>2'`. Number values are unquoted.
- **`LIKE` is prefix-only** — exactly one trailing `%`. Invalid: `'%x%'`, `'%x'`, `'x%y'`. Rejects `: ^ { } [ ] ( )`, so `LIKE 'https:%'` fails on the colon. (The character list is documented on the hybrid page; assume it applies to vector too.)
- **Field names case-insensitive, values case-SENSITIVE.** `Col='somevalue'` against stored `SomeValue` returns zero rows with no error. First thing to check on an unexpectedly empty result.
- Supported: `= != < > >= <= IN NOT IN LIKE AND OR` with parentheses.
- **1:N relationships lose data** — only one prefilter value is indexed per chunk, nondeterministically. Multi-valued tag filtering does not work.

## Fusion ranking (hybrid only)

Retrieve from both indexes → merge → rerank. `hybrid_score__c` is a weighted blend of normalized keyword and vector scores plus ranking factors.

Two facts that drive design decisions:

1. **A zero keyword score can still rank #1.** Fusion is a blend, not a gate.
2. **Scores are comparable only within one query.** Never threshold on an absolute value (`WHERE hybrid_score__c > 0.7`), and never sort scores from two different indexes together — keyword scores are corpus-relative (BM25 IDF) and vector scores are model-relative.

`keyword_score__c` is unbounded (BM25-style, typically 1–10). `vector_score__c` and `hybrid_score__c` are 0–1.

**Diagnostic worth running once:** compare the spread of `vector_score__c` vs `hybrid_score__c` across the same result set. e5-family embeddings compress similarities into a narrow band (~0.01 spread is common), so vector alone barely ranks. If fusion widens the spread substantially, hybrid is earning its keep.

### Relevance configuration (5th argument)

```sql
'{ "rrf": { "keyword_weight": 0.4 } }'   -- rank-based, scale-agnostic, safe default
'{ "dfr": {} }'                          -- transformer reranker, no knobs, best quality
'{ "lfr": { "vector":  {"score_transform": {"type":"reciprocal_rank","decay":60}, "weight":0.669},
            "keyword": {"score_transform": {"type":"query_min_max","theoretical_min":0}, "weight":4.034} } }'
```

Selection rule: **DFR** when you want quality with no tuning budget. **RRF** when score scales are incomparable or you want a well-understood baseline. **LFR** only with real relevance judgments to tune against — otherwise you degrade the fine-tuned default.

RRF sums the keyword and vector reciprocal-rank scores with a default decay of **k=60**. `keyword_weight`
ranges 0–1, and the vector weight is 1 − `keyword_weight`.

RRF advanced coefficients: α keyword (0.5), β vector (1−α), γ popularity (0.00074478, max 1), δ recency (0.00028472, max 1). The ~1e-4 defaults are deliberate — popularity/recency are raw magnitudes that would otherwise swamp relevance. Tweak in small increments. The docs don't give the JSON key names for α/γ/δ, so don't invent them.

LFR weights are only meaningful **relative to their paired transform** — asymmetric weights usually compensate for different output scales, not a deliberate keyword/vector bias.

LFR transforms:

- `reciprocal_rank` takes a `decay` parameter and computes `score = 1/(rank + decay)`. A smaller decay
  spreads adjacent ranks further apart.
- `query_min_max` takes `theoretical_min`. For keyword, the docs' own prose says 0 is correct and you
  shouldn't change it without data. The docs' LFR example uses `"theoretical_min": 0.1`, which
  contradicts that, so don't copy the example value from help.salesforce.com.

DFR also uses popularity and recency, adds a transformer model's reading of the query text, and is
documented as robust to missing or noisy data.

## Autodrop

Truncates at score cliffs instead of always filling `k`. Without it, ANN always returns exactly `k` results regardless of quality — padding a RAG prompt with noise. (The keyword leg is different: it returns only documents that contain query terms, so it can come back with fewer than `k`.)

**Autodrop is available only with `hybrid_search()`** and is **disabled by default**. There is no
autodrop for a standalone `vector_search()` call — `autodrop_vector` configures the vector *leg inside*
hybrid search, not the separate function. If you need quality-based truncation, that alone is a reason
to build the index as `HYBRID`.

```sql
'{ "autodrop_keyword": {"num_drops": 2}, "autodrop_vector": {"num_drops": 5} }'   -- documented recommendation
'{ "autodrop_hybrid": {"num_drops": 3} }'                                        -- works, but see caveat
```

Use **either** hybrid **or** the keyword+vector pair — never all three.

**Prefer the keyword+vector pair.** The [autodrop best-practices article](https://help.salesforce.com/s/articleView?id=data.c360_a_hybridsearch_autodrop_best_practices.htm&type=5)
says that, because of how fused hybrid scores are distributed, `autodrop_hybrid` "can lead to
unexpected behavior". It recommends `autodrop_keyword: 2` and `autodrop_vector: 5` as the starting
point. `autodrop_hybrid` isn't broken: it was calibrated and shipped on a real index (see the worked
example). If you use it, calibrate with the sweep below and re-check after ingestion.

**Higher `num_drops` = more permissive** (more results), not stricter. It counts score cutoff points you
are willing to fall past. The docs now state this explicitly ("To make hybrid search autodrop less
aggressive and retain more results, consider increasing the num_drops value"), and it has also held
up in repeated testing. Other documented behaviour:

- **If `num_drops` exceeds the actual number of score drops**, no truncation happens. You get the full
  `k` rows, with no error.
- **Keyword-side autodrop** is specifically useful when many documents share the same terms.
- **Tune the leg that's losing results.** If relevant results go missing, raise `num_drops` on that
  leg. If noise remains, lower it.

### Do not try to predict cut points from the scores

The cutoff-detection rule is undocumented. Even the docs' own worked example isn't self-consistent: it
lists a "descending" score sequence with 0.80 after 0.10. Attempts to reverse-engineer the rule from
score gaps have
**failed empirically**. On one real index, `num_drops: 3` cut at an adjacent-score gap of 0.0204 while
`num_drops: 4` did **not** cut at a later gap of 0.0591. No absolute or relative gap threshold explains
both — a model fitted to four observations mispredicted the fifth (predicted 11 rows, actual 7).

Treat the detector as a black box. Do not compute gaps, do not derive thresholds, and do not promise a
user a specific row count for a given `num_drops`.

### Calibrate empirically instead

Sweep the values and record raw row counts — no joins, no `GROUP BY`, no `LIMIT`:

```sql
-- documented default: sweep one leg at a time around keyword 2 / vector 5
select * from hybrid_search(TABLE(<Index_DMO>), '<question>', '', 30,
  '{ "autodrop_keyword": {"num_drops": K}, "autodrop_vector": {"num_drops": V} }')

-- or, if using the fused score
select * from hybrid_search(TABLE(<Index_DMO>), '<question>', '', 30,
  '{ "autodrop_hybrid": {"num_drops": N} }')
```

A representative `autodrop_hybrid` sweep from a real index (same query, k=30):

| `num_drops` | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| rows | 2 | 4 | 7 | 12 |

Then pick the value that lands in your target band. With `k=30` and `LIMIT 6`, reasonable starting
points for RAG are keyword 2 / vector 5 (documented), or `autodrop_hybrid: 3` (empirically validated
on one index).

Other behaviour notes:

- **Autodrop truncates BEFORE your `GROUP BY` dedups.** Duplicates consume the budget, so N retrieved
  becomes fewer unique. Over-fetch to compensate.
- **The mapping is query-specific and corpus-specific.** Calibrate against 5–10 varied real questions —
  narrow factual, broad conceptual, and deliberately off-topic. A single query overfits, especially one
  with clustered near-duplicate content.
- **Scores drift as the corpus changes**, so a calibration can go stale. `vector_score__c` is pairwise
  and stable across index refreshes; `keyword_score__c` depends on corpus-wide term statistics and
  shifts when documents are added or changed, moving `hybrid_score__c` with it. Re-check after
  significant ingestion.
- Adaptive result counts give you a free "no answer" signal: if fewer than N chunks return, respond
  "I don't have information on that" rather than answering from one weak passage. Verify this by
  sweeping a deliberately off-topic question.

## Multiple indexes

Not supported natively — `hybrid_search()` takes exactly one `TABLE()`. Nothing in the Help documentation describes a multi-index form.

Workarounds, in order of soundness:

1. **Query separately from the application and merge there.** Best control, avoids the score-comparability trap.
2. **`UNION ALL` + rank-based (RRF) merge in SQL** — `SUM(1.0/(60 + rnk))` over `ROW_NUMBER() OVER (ORDER BY hybrid_score__c DESC)` per branch. Rank is scale-free so it survives crossing index boundaries. (Window-function support not verified.)
3. **`UNION ALL` + `ORDER BY score`** — looks principled, is not. Only acceptable for rough exploration.

If the indexes cover the same content and you are unioning for recall, they should probably be one index with a prefilter instead.

## Running the SQL from Apex

Use the **`sfsqlquery`** namespace (`SqlStatement.create(sql, 'default').withWorkloadName(...).execute()`,
then iterate `Row`s). It runs `hybrid_search()` with joins and autodrop in about 0.5 s with no callouts,
and comes with a test mock (`SqlTester`). `ConnectApi.CdpQuery.queryAnsiSqlV2` is the older low-level option.

The rules that matter most:
- **Escape the search text**: double every `'`, strip control characters, cap the length.
- **Alias every column** and read rows by alias: an unknown column name throws.
- Run `unescapeHtml4()` on text, because it can come back HTML-escaped.
- **Queries run as the calling user.** Inside an agent, that's the agent user, which needs Apex class access
  and Data 360 access. If the class swallows errors, a missing permission looks like "no results" everywhere.
- **As a Prompt Builder Flex data provider:** `@InvocableMethod` with **no** `CapabilityType`, `Request.query`
  named exactly like the template input, and `Response` with a single `String Prompt`.

Full guide, including the template metadata, the version-publishing steps, and `SqlTester` mocks with the
fields that actually compile: `references/apex-sfsqlquery.md`.
A complete production retriever class (anonymised), with the reason behind each pattern: settings-driven
DMO names, chunk deduplication, boilerplate filters, email removal and link fixing:
`references/example-apex-retriever.md`.

## Keyword-search traps (observed on a Norwegian index)

These explain "the passage exists but hybrid search won't find it". Check them before tuning anything else:
- **No stemming and no compound-word splitting.** "powerbank" scored 0 against "Powerbanks"; "alkohol"
  didn't match "Alkoholkvote". The vector side doesn't rescue it, because e5 scores cluster within about 0.01.
- **The keyword side requires most query words to match.** One unmatched word lowered the keyword score;
  two zeroed the keyword results entirely.
- **Keyword results vary between identical runs.** One query scored 11.45, then 0, minutes apart.
- **So don't append keyword lists to the query** (a "Søkeord: …" expansion was tried and reverted): it fixes
  some questions, breaks others, and can't be tuned reliably.
- **Cross-language gaps:** an English question ("dog to Kiel") missed a Norwegian-only passage
  ("…mellom Norge og Tyskland…") even with a multilingual embedding model.
- **Page-chrome noise:** crawled sites index icon-name lists, navigation and repeated footers. On one sitemap
  index that was 28% of chunks. Exclude it in the outer `WHERE` (`NOT LIKE` patterns and a minimum
  `LENGTH(Chunk__c)`) and measure the share first. Use `_` for non-ASCII letters in `LIKE` patterns.

## Index coverage: check it before blaming the query

```sql
SELECT COUNT(DISTINCT SourceRecordId__c) FROM <Chunk_DMO>   -- compare with SELECT COUNT(*) FROM <Source_DMO>
```

If only a few source records have chunks, the problem is the index, not the SQL. On one sitemap (web crawler)
connector, the index **only parsed files from the newest crawl run**. Unchanged pages kept pointing at older
crawl folders (`SPLIT_PART(FilePath__c,'/',3)`), and those files failed with "Tolerance limit exceeded for
Parsing failure", while the UI showed Ready or FAILED with no reason. `FULL_REFRESH` didn't re-crawl unchanged
pages. The workaround was a brand-new data stream, indexed straight after its first crawl. Group the source
rows by crawl folder against chunk coverage to diagnose it.

For a non-English site, choose a **multilingual** embedding model. E5 Large V2 and SFR-v2-small are
English-only.

## Recurring failure modes

| Symptom | Cause |
|---|---|
| Unresolved column `KQ_RecordId__c` | Not projected by the search function; drop the predicate |
| Rung 1 works, Rung 2 empty | Wrong index→chunk key; `SourceRecordId__c` is documented, `RecordId__c` is the fallback |
| Rung 2 works, Rung 3 empty | Wrong chunk→source key; run the match-count diagnostic |
| Prefilter returns zero, no error | Value case mismatch, or field not registered at index creation |
| Date prefilter fails after copy-paste | Quoted in `vector_search`, unquoted in `hybrid_search` |
| Row count ≫ k | Fan-out from duplicate source rows; dedup or `GROUP BY` |
| Top results are the same passage repeated | Near-duplicate document versions; exact-text `GROUP BY` won't merge them |
| Scores nearly identical across results | Normal for e5 embeddings; use hybrid + autodrop, never an absolute threshold |
| `Chunk__c` returns keyword lists, summaries or questions | Enriched index: QUESTION/METADATA hits. Map them to the PLAIN passage via `COALESCE(NULLIF(h.SourceChunks__c,''), h.SourceRecordId__c)` |
| Same passage fills three slots | Enriched index: the PLAIN, QUESTION and METADATA chunks of one passage. Map to the passage, then `GROUP BY` it |
| Enriched mapping drops every PLAIN hit | `COALESCE` without `NULLIF`: `SourceChunks__c` is `''` on PLAIN, not NULL |
| `unknown column 'ChunkProcessingType__c'` | The index isn't enriched; use the standard join |
| Autodrop returns full `k`, no truncation | `num_drops` exceeds the number of score drops detected, or autodrop JSON not applied |
| Autodrop cuts erratically across queries | `autodrop_hybrid` on fused scores; switch to `autodrop_keyword` + `autodrop_vector` |

## Content-quality issues no query can fix

Flag these to the user rather than tuning around them:

- **Superseded document versions** all indexed together (e.g. four vintages of the same T&Cs). Vector similarity has no concept of "current". Correct fixes, in order: exclude archived versions from the stream; add a **recency ranking factor** on a last-modified field at index config; failing both, an outer `WHERE` on a date field. Near-duplicate text defeats exact-match `GROUP BY` because versions differ by trivial prefixes.
- **Citations pointing at CDN asset URLs** with blank titles when content lives in PDFs rather than crawled pages. Fall back through `COALESCE(NULLIF(Title__c,''), FileName__c, URL__c)`, or restrict to real pages with a URL `LIKE` filter.

### Chunking causes visible in query results

These are diagnoses only. Fixing them means changing the index configuration, which is outside this
skill's scope. Sources: the [chunking strategies](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_supported_chunking_strategies.htm&type=5)
and [max token](https://help.salesforce.com/s/articleView?id=data.c360_a_search_index_max_token_setting.htm&type=5) articles.

- **Tiny fragment chunks** (one list item or a short line each). Section-aware chunking, the default for
  HTML and PDF in the advanced builder, sometimes treats short paragraphs or list items as headings.
  The fix is to raise Max Token so that adjacent small sections merge.
- **Weak relevance on non-Latin content** (for example Japanese). Data 360 estimates tokens from
  punctuation marks for non-Latin languages, so a 512-limit chunk can exceed the embedding model's
  limit. The model silently ignores the overflow. The fix is a Max Token below the default of 512.
  Latin-script languages (Norwegian, English) estimate one word per token and are usually fine.
- **Chunk text starts with a title, URL or file path.** Those are prepend fields set at index
  configuration. They're part of `Chunk__c`, so they affect exact-text `GROUP BY` and what the LLM sees.
  If the prepended fields exceed 512 tokens, Data 360 skips the prepend altogether.
- **Audio and video transcripts** are chunked per speaker turn, so each chunk is often a single short
  utterance.
- **`ChunkSequenceNumber__c`** starts at 0 according to the Chunk DMO reference, but the chunking-strategy
  examples number from 1. Check the actual data before relying on position 0.

## Reference

`references/worked-example.md` — a complete, verified end-to-end build against a real index, showing each rung's actual output and how the join key was found.

`references/apex-sfsqlquery.md` — running the SQL from Apex with `sfsqlquery`, as a Prompt Builder Flex data provider, and testing it with `SqlTester`.

`references/example-apex-retriever.md` — a complete, anonymised production retriever class used as both a Flex template data provider and an Agent Script `apex://` action, with a table of its patterns and the evidence behind them.
