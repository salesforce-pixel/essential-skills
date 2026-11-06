# Worked example — AcmeTravel sitemap index

A complete, verified build against a real Data 360 hybrid search index over a crawled travel site
(web pages plus Contentful-hosted PDF assets). Every query below was executed in the Data Cloud
Query Editor; the outputs are real. Use this to see what each rung of the discovery ladder actually
returns, and how a wrong join-key guess gets corrected.

## The objects

| Role | API name | Category | Fields |
|---|---|---|---|
| Source | `AcmeTravel_Sitemap_EN_GB__dlm` | `DIRECTORY_TABLE` | 27 |
| Chunk | `AcmeTravel_Sitemap_EN_GB_chunk__dlm` | `CONTENT` | 14 |
| Index | `AcmeTravel_Sitemap_EN_GB_index__dlm` | `VECTOR_EMBEDDING` | 9 |

Index DMO fields (all 9): `ContextField__c`, `DataSource__c`, `DataSourceObject__c`,
`InternalOrganization__c`, `KQ_RecordId__c`, `KQ_SourceRecordId__c`, `RecordId__c`,
`SourceRecordId__c`, `VectorEmbedding__c`.

Note the drift from the published reference: this instance adds `ContextField__c` and
`KQ_SourceRecordId__c`, neither of which appears in the Index DMO doc. The chunk DMO likewise carries
`Citations__c` (plural, vs documented `Citation__c`) plus `ChunkFormat__c`, `ChunkType__c`,
`MediaSource__c` and `SecondarySourceRecordId__c`. Read the real field list; don't assume the doc's.

That list is the whole story on prefiltering: **no business fields were registered**, so
`Language__c`, `ContentType__c`, `LastModified__c` and `URL__c` are unavailable as prefilter
arguments. All narrowing has to happen in an outer `WHERE`.

The source is a `DIRECTORY_TABLE` with **no `Id__c` column** — its identity fields are
`FilePath__c`, `ExternalSourceId__c`, `Hash__c`, `URL__c`, `OriginalFilePath__c`,
`ResolvedFilePath__c`.

## Rung 1 — smoke test

```sql
SELECT * FROM vector_search(
  TABLE(AcmeTravel_Sitemap_EN_GB_index__dlm),
  'how do I cancel my booking', '', 5)
```

5 rows, 432 ms. Columns returned: `ContextField__c`, `DataSource__c`, `RecordId__c`,
`SourceRecordId__c`, `VectorEmbedding__c`, `score__c`.

Two immediate findings:

- **No `KQ_RecordId__c` in the output**, despite it existing on the index DMO. The join predicate
  the Salesforce docs show (`c.KQ_RecordId__c IS NOT DISTINCT FROM v.KQ_RecordId__c`) would fail
  here with an unresolved column.
- `RecordId__c` and `SourceRecordId__c` held **identical values** in every row. Per the Index DMO
  reference these are semantically distinct — `RecordId__c` is the embedding's own PK, while
  `SourceRecordId__c` is documented to match `chunk.RecordId__c`. This index happens to populate them
  identically, which is why joining on either worked below. Prefer `SourceRecordId__c` on a new index.

`DataSource__c` came back as the literal string `FilePath__c` on every row. That is not a data-source
system name — per the docs it is the **API name of the field that was chunked**, so this index chunks
content addressed by `FilePath__c`. It is also a default pre-filtering field.

Scores: `0.8522, 0.8515, 0.8480, 0.8480, 0.8476` — a 0.005 spread. Rows 3 and 4 had byte-identical
`VectorEmbedding__c` values, i.e. genuine duplicate content.

## Rung 2 — chunk text

```sql
SELECT v.score__c AS Score__c, c.Chunk__c AS Chunk__c
FROM vector_search(
  TABLE(AcmeTravel_Sitemap_EN_GB_index__dlm),
  'how do I cancel my booking', '', 5) v
JOIN AcmeTravel_Sitemap_EN_GB_chunk__dlm c
  ON v.RecordId__c = c.RecordId__c
ORDER BY v.score__c DESC
```

5 rows, 268 ms. Relevant cancellation-policy passages. Retrieval confirmed working.

## Rung 3 — finding the chunk→source key

**The wrong guess first.** The source being a `DIRECTORY_TABLE` with a `FilePath__c` column matches
the UDMO pattern in the Salesforce docs (`ON c.SourceRecordId__c = u.FilePath__c`), so that was the
obvious candidate. It returned **zero rows**.

Diagnostic A:

```sql
SELECT c.SourceRecordId__c, c.KQ_SourceRecordId__c, c.DataSourceObject__c, c.MediaSource__c
FROM AcmeTravel_Sitemap_EN_GB_chunk__dlm c LIMIT 5
```

| `SourceRecordId__c` | `MediaSource__c` |
|---|---|
| `0c603fadd8d9c4e496680e4b4fcf3891405c8fe0` | *(null)* |
| `4909f6b3e6834f324a27e290f3242b5666ff6859` | `AcmeTravel_Sitemap_EN_GB__dll:uEkSitemap/9cgb…` |

40-char hex — a hash, **not** a path. `MediaSource__c` does embed the FilePath, but it is NULL on
3 of 5 rows, so it is evidence rather than a join key.

Diagnostic B:

```sql
SELECT FilePath__c, ResolvedFilePath__c, OriginalFilePath__c, ExternalSourceId__c, URL__c
FROM AcmeTravel_Sitemap_EN_GB__dlm LIMIT 5
```

| Column | Sample |
|---|---|
| `FilePath__c` | `uEkSitemap/9cgba0000000AKLAA2/8…` |
| `OriginalFilePath__c` | `https://images.eu.ctfassets.net/<space-id>…` |
| `ExternalSourceId__c` | `001303f26c8b5e9122c673af5dc1ffb3…` ← hex, matching shape |

Diagnostic C — settle it with counts:

```sql
SELECT 'ExternalSourceId__c' AS Candidate, COUNT(*) AS Matches
FROM AcmeTravel_Sitemap_EN_GB_chunk__dlm c
JOIN AcmeTravel_Sitemap_EN_GB__dlm s ON c.SourceRecordId__c = s.ExternalSourceId__c
UNION ALL
SELECT 'Hash__c', COUNT(*)
FROM AcmeTravel_Sitemap_EN_GB_chunk__dlm c
JOIN AcmeTravel_Sitemap_EN_GB__dlm s ON c.SourceRecordId__c = s.Hash__c
```

| Candidate | Matches |
|---|---|
| `ExternalSourceId__c` | **13432** |
| `Hash__c` | 0 |

`ExternalSourceId__c` is the key. The large count signalled table-wide fan-out, but the full query
returned exactly 10 rows for `k=10`, so the retrieved chunks were unaffected.

## Rung 4 — hybrid probe

```sql
SELECT h.vector_score__c, h.keyword_score__c, h.hybrid_score__c, s.URL__c, c.Chunk__c
FROM hybrid_search(
  TABLE(AcmeTravel_Sitemap_EN_GB_index__dlm),
  'how do I cancel my booking', '', 10) h
JOIN AcmeTravel_Sitemap_EN_GB_chunk__dlm c ON h.SourceRecordId__c = c.RecordId__c
JOIN AcmeTravel_Sitemap_EN_GB__dlm s ON c.SourceRecordId__c = s.ExternalSourceId__c
ORDER BY h.hybrid_score__c DESC
```

Hybrid confirmed live. Note `h.SourceRecordId__c` for the chunk join, versus `v.RecordId__c` for
vector search.

**Fusion demonstrably outperformed vector alone on the same 10 results:**

| | Range | Spread |
|---|---|---|
| `vector_score__c` | 0.8408 – 0.8522 | **0.011** |
| `hybrid_score__c` | 0.7930 – 0.9725 | **0.179** |

Vector alone compressed everything into a 1% band — effectively refusing to rank. Fusion widened
that ~16×. It also **reordered**: the chunk with the *lowest* vector score in the set (0.8430,
`IF WE CHANGE OR CANCEL YOUR BOOKING`) rose to hybrid rank 7 on the strength of the highest keyword
score (5.93). Pure vector was under-ranking it.

`keyword_score__c` ranged 5.14–5.93 — unbounded BM25-style, not 0–1.

## Autodrop calibration

Raw row counts, same query, `k=30`, no joins or `LIMIT`:

| `num_drops` | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| rows | 2 | 4 | 7 | 12 |

Monotonic, as documented. That is the reliable part.

> **Note (added Oct 2026):** this calibration used `autodrop_hybrid`. Salesforce's
> [autodrop best-practices article](https://help.salesforce.com/s/articleView?id=data.c360_a_hybridsearch_autodrop_best_practices.htm&type=5)
> recommends `autodrop_keyword` + `autodrop_vector` (starting at 2 / 5) instead. It says the
> distribution of fused hybrid scores can make `autodrop_hybrid` behave unexpectedly. The results
> below are a real run and still stand. For a new index, start with the keyword+vector pair and sweep
> it the same way.

### Why gap-threshold reasoning was abandoned

Hybrid scores from the `num_drops: 4` run, ranks 1–12:

```
0.97318  0.94226  0.91024  0.91024  0.83728  0.83040
0.82561  0.80523  0.79303  0.79303  0.76510  0.70598
```

`num_drops: 3` returned 7 rows, so its cutoff falls at the rank 7→8 gap of **0.0204**.
`num_drops: 4` returned 12 rows, so the rank 11→12 gap of **0.0591** was *not* a cutoff.

No absolute threshold makes 0.0204 significant and 0.0591 not. Relative-to-preceding-score fails the
same way (2.5% vs 7.7%). A threshold model fitted to the 1/2/4 observations predicted 11 rows for
`num_drops: 3`; the actual answer was 7.

**Conclusion: treat cutoff detection as a black box and calibrate empirically.** Do not compute gaps
or promise row counts.

### Dedup interaction

At `num_drops: 2`, two of the four returned rows were the duplicate pair (`cf401a70…` and
`cf876624…`, identical hybrid scores to 16 digits), leaving only **3 unique** chunks after
`GROUP BY`. Autodrop truncates before dedup; both spend from the same budget.

`num_drops: 3` (7 raw) with `GROUP BY` and `LIMIT 6` yielded 6 unique chunks. That was the setting
shipped.

### Score drift between runs

The same query run a day apart returned bit-identical `vector_score__c` values but shifted
`keyword_score__c` (5.52507209777832 → 5.552648544311523), moving `hybrid_score__c` with it. Vector
similarity is pairwise between query and chunk and so is corpus-independent; BM25-family keyword
scoring depends on corpus-wide term statistics and moves when documents are added or changed.

Consequence: a `num_drops` calibration is a snapshot. Re-check after significant ingestion.

## Final query

```sql
SELECT
  MAX(h.hybrid_score__c) AS Score__c,
  MAX(s.URL__c)          AS URL__c,
  c.Chunk__c             AS Chunk__c
FROM hybrid_search(
  TABLE(AcmeTravel_Sitemap_EN_GB_index__dlm),
  'how do I cancel my booking',
  '',
  30,
  '{ "autodrop_hybrid": {"num_drops": 3} }'  -- see note under Autodrop calibration; docs recommend the keyword/vector pair
) h
JOIN AcmeTravel_Sitemap_EN_GB_chunk__dlm c
  ON h.SourceRecordId__c = c.RecordId__c
JOIN AcmeTravel_Sitemap_EN_GB__dlm s
  ON c.SourceRecordId__c = s.ExternalSourceId__c
GROUP BY c.Chunk__c
ORDER BY MAX(h.hybrid_score__c) DESC
LIMIT 6
```

6 rows, 109 ms.

## Unresolved content issues

Two problems surfaced that query tuning could not fix, worth recognising early on similar corpora.

**Superseded document versions.** Adding `FileName__c` to the projection revealed that the top
results were the same cancellation clause drawn from four vintages of the same T&Cs document:

```
18_March_2024_Update_-_HX_General_T_Cs_-_…
HX_General_T_Cs_-_UK_-_Effective_03-11-2025…   ← current
HX_General_T_Cs_-_UK_-_Effective_01-11-2024…
2023-09-04_Updated_General_terms_and_condi…
```

`GROUP BY c.Chunk__c` does not merge them, because the versions differ by trivial prefixes
(`IF YOU CANCEL…` / `7. IF YOU CANCEL…` / `IF YOU CANCEL BEFORE DEPARTURE7.`). Half the context
budget went to one repeated clause, and a RAG answer could cite a superseded policy. The proper fix
is a **recency ranking factor** at index config, or excluding archived versions from the stream —
not query tuning.

**Asset URLs as citations.** 9 of 10 results resolved to `assets.ctfassets.net/…` with a blank
`Title__c`, because the policy content lives in Contentful-hosted PDFs rather than crawled pages.
`COALESCE(NULLIF(s.Title__c,''), s.FileName__c, s.URL__c)` produced usable labels;
`WHERE s.URL__c LIKE 'https://www.example-travel.com%'` (with a raised `k`) restricts to real pages.

## Verified SQL features

Confirmed working in the Data Cloud Query Editor during this build: `COALESCE`, `NULLIF`,
`UNION ALL`, `GROUP BY`, `MAX()`, `LIKE`, `ORDER BY <aggregate> DESC`, table functions in `JOIN`
position, `DATE` literals in an outer `WHERE`.

Not tested: CTEs (`WITH`), window functions (`ROW_NUMBER() OVER`), `SELECT DISTINCT` on large
projections.
