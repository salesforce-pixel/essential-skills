# Example: a complete Apex retriever (Prompt Builder data provider and agent action)

A production class from a website FAQ agent, anonymised: Acme and example.com stand in for the customer, and
the index names are placeholders. It ran against a hybrid index of about 4,400 crawled pages and PDFs
(34k chunks), verified October–November 2026. It's called both as a Flex template data provider
(`{!$Apex:AcmeWebsiteRetriever.Prompt}`) and directly from an Agent Script action
(`target: "apex://AcmeWebsiteRetriever"`, input `Question`, output `Prompt`).

Use it as a starting point; the patterns and the numbers behind them are what matter:

| Pattern | Where | Why |
|---|---|---|
| Index, chunk and source DMO names and the data space come from a Custom Metadata record, with code defaults | `indexDmo()`, `settingValue()` | Each org can point at its own index, or switch to a parallel index (never rebuild a live one), without a code change. |
| Setting values must match `^[A-Za-z][A-Za-z0-9_]*__dlm$` | `DMO_NAME`, `settingValue()` | They're written into the SQL text, so anything else throws instead of running altered SQL. |
| `hybrid_search(TABLE(index), q, '', 30, autodrop)` then index → chunk → source join | `buildSearchSql()` | Over-fetch 30, keep 8. Keyword 1 / vector 1 autodrop cut real answers to 2 passages; k=60 changed nothing. |
| `GROUP BY c.Chunk__c` with `MAX()` on the rest | `buildSearchSql()` | Identical chunk text repeats on many pages (only 19k of 34k chunk texts were distinct). |
| Page chrome removed in the outer `WHERE`, after autodrop | `EXCLUDED_CHUNK_PATTERNS`, `buildChunkFilter()` | Login wall, state picker, contact forms and footers were about 39% of all chunks. The patterns are site-specific; find yours with `GROUP BY Chunk__c ORDER BY COUNT(*) DESC`. |
| `COALESCE(NULLIF(Title__c, ''), FileName__c)` | `buildSearchSql()` | PDFs from the web crawl have a blank title. |
| Escape the question: control characters out, whitespace collapsed, 500-character cap, `'` doubled | `cleanQuestion()`, `toSqlLiteral()` | It's the only user-supplied value in the SQL. |
| `unescapeHtml4()` on title and text | `unescape()` | Text can come back HTML-escaped (`&#124;`). |
| Email addresses removed from every passage | `EMAIL_PATTERN`, `removeEmails()` | About 800 chunks held office and personal addresses. An instruction alone didn't stop the agent from quoting them; if the model never sees the address, it can't repeat it. |
| Site-relative links made absolute | `absolutizeLinks()` | Crawled chunks keep `Read More (/en/...)`, which the LLM would hand on as broken links. |
| Numbered excerpts with `Title:` and `URL:` lines | `formatPassages()` | The prompt or agent can cite the right page for each fact. |
| Every failure returns the same no-results text | `retrieveGroundingText()` | The visitor never sees an error. Downside: traces can't tell an error from an empty result, and a missing permission looks like "no results" everywhere. Consider a distinct marker if you need to monitor it. |
| Only `requests[0]` is searched | `getPrompt()` | Prompt Builder sends one request; extra elements get the no-results text. |

Tests mock Data 360 with `sfsqlquery.SqlTester` (see `apex-sfsqlquery.md`) and set the `@TestVisible`
`setting` field to an in-memory record, or to `null` for the defaults. The agent user needs class access
to the class, Data 360 access to the data space, and `customMetadataTypeAccesses` for the settings type.

```apex
/**
 * Prompt Builder data provider for the Flex template Acme_Website_FAQ.
 * Retrieves the most relevant passages from the example.com search index in Data 360
 * using hybrid_search() SQL, and returns them as formatted grounding text for the prompt.
 *
 * The standard Einstein retriever only returns page-level fields (title, meta description),
 * so the matched passage text never reaches the LLM. This class returns the passages themselves.
 *
 * Contract (Flex templates): no CapabilityType; Request fields must match the template input
 * API names (Question); Response has a single String member named Prompt.
 * Changing the Request fields breaks the template, so keep them stable.
 *
 */
public with sharing class AcmeWebsiteRetriever {

    // Search index objects come from the Acme_Retriever_Setting__mdt record "Default", so each
    // org can point at its own index. These values are used when that record doesn't exist.
    @TestVisible private static final String SETTING_RECORD = 'Default';
    @TestVisible private static final String DEFAULT_INDEX_DMO = 'Acme_Website_SI_index__dlm';
    @TestVisible private static final String DEFAULT_CHUNK_DMO = 'Acme_Website_SI_chunk__dlm';
    @TestVisible private static final String DEFAULT_SOURCE_DMO = 'Acme_Website__dlm';
    @TestVisible private static final String DEFAULT_DATA_SPACE = 'default';
    // Setting values are placed in the SQL text, so only plain API names are accepted.
    private static final Pattern DMO_NAME = Pattern.compile('^[A-Za-z][A-Za-z0-9_]*__dlm$');
    private static final Pattern DATA_SPACE_NAME = Pattern.compile('^[A-Za-z][A-Za-z0-9_]*$');

    @TestVisible
    private static Acme_Retriever_Setting__mdt setting = Acme_Retriever_Setting__mdt.getInstance(SETTING_RECORD);

    private static final String WORKLOAD_NAME = 'acme_website_retriever';
    private static final String SITE_ROOT = 'https://www.example.com';

    // Retrieval tuning: over-fetch, cut at score drops, then keep the best unique passages.
    // Calibrated on spot tests: keyword 1 / vector 1 cut real answers to 2 passages, and
    // fetching 60 candidates instead of 30 changed nothing.
    private static final Integer CANDIDATE_COUNT = 30;
    private static final Integer MAX_PASSAGES = 8;
    private static final String RELEVANCE_CONFIG =
        '{ "autodrop_keyword": {"num_drops": 2}, "autodrop_vector": {"num_drops": 5} }';
    // Crawled page chrome repeated on every page (about 39% of chunks): login wall, US state
    // picker, contact forms, "Get in touch" footer, process navigation, and product tab strips.
    private static final List<String> EXCLUDED_CHUNK_PATTERNS = new List<String>{
        'Login to get full access%',
        'State Alabama Alaska%',
        '%First name Last name Email Phone Company%',
        'Get in touch Our dedicated team%',
        'Select your process Select your process%',
        'Information Service%',
        'Information Versions%',
        'Information Specifications%',
        'Information Software%'
    };
    private static final Integer MIN_CHUNK_LENGTH = 40;

    private static final Integer MAX_QUESTION_LENGTH = 500;

    // Email addresses (with an optional mailto: prefix) are removed from every passage, so the agent
    // can't repeat them. About 800 chunks hold office and personal addresses, mostly from PDF brochures.
    private static final String EMAIL_PATTERN =
        '(?i)(mailto:)?[a-z0-9._%+-]+@[a-z0-9-]+(\\.[a-z0-9-]+)*\\.[a-z]{2,}';

    @TestVisible
    private static final String NO_RESULTS_TEXT =
        'No relevant content was found on example.com for this question.';

    /**
     * Returns grounding text from the Acme website for the visitor's question.
     * Prompt Builder sends exactly one request; only the first element carries data.
     * @param requests Prompt template inputs; requests[0].Question is the visitor's question
     * @return One Response per request, each with the grounding text in Prompt
     * @example
     * AcmeWebsiteRetriever.Request req = new AcmeWebsiteRetriever.Request();
     * req.Question = 'Do you have any customer stories from Belgium?';
     * String grounding = AcmeWebsiteRetriever.getPrompt(new List<AcmeWebsiteRetriever.Request>{ req })[0].Prompt;
     */
    @InvocableMethod(
        label='Acme Website Retriever'
        description='Returns passages from example.com that are relevant to the visitor question, for grounding a prompt template.'
        category='Prompt Builder'
    )
    public static List<Response> getPrompt(List<Request> requests) {
        List<Response> responses = new List<Response>();
        if (requests == null || requests.isEmpty()) {
            return responses;
        }

        String groundingText = retrieveGroundingText(requests[0]?.Question);
        for (Integer i = 0; i < requests.size(); i++) {
            Response output = new Response();
            output.Prompt = (i == 0) ? groundingText : NO_RESULTS_TEXT;
            responses.add(output);
        }
        return responses;
    }

    /**
     * Runs the search and formats the passages. Any failure returns the no-results text,
     * so the prompt tells the visitor it has no answer instead of surfacing an error.
     */
    private static String retrieveGroundingText(String question) {
        String cleanQuestion = cleanQuestion(question);
        if (String.isBlank(cleanQuestion)) {
            return NO_RESULTS_TEXT;
        }

        try {
            List<Passage> passages = queryPassages(buildSearchSql(cleanQuestion));
            return passages.isEmpty() ? NO_RESULTS_TEXT : formatPassages(passages);
        } catch (Exception e) {
            System.debug(LoggingLevel.ERROR,
                'AcmeWebsiteRetriever search failed: ' + e.getTypeName() + ': ' + e.getMessage());
            return NO_RESULTS_TEXT;
        }
    }

    /**
     * Executes the Data 360 SQL and maps rows to passages.
     */
    private static List<Passage> queryPassages(String sqlText) {
        List<Passage> passages = new List<Passage>();
        sfsqlquery.SqlRowIterator rows = sfsqlquery.SqlStatement.create(sqlText, dataSpace()).withWorkloadName(WORKLOAD_NAME).execute();
        for (sfsqlquery.Row row : rows) {
            Passage passage = new Passage();
            passage.title = removeEmails(unescape(row.getString('Title__c')));
            passage.url = row.getString('URL__c');
            passage.text = absolutizeLinks(removeEmails(unescape(row.getString('Chunk__c'))));
            if (String.isNotBlank(passage.text)) {
                passages.add(passage);
            }
        }
        return passages;
    }

    /**
     * Builds the hybrid_search SQL. The question is the only user-supplied value and is
     * embedded as an escaped SQL string literal. PDFs have no title, so the file name stands in.
     * @param cleanQuestion Question already passed through cleanQuestion()
     * @return Data 360 SQL text
     */
    @TestVisible
    private static String buildSearchSql(String cleanQuestion) {
        return 'SELECT MAX(h.hybrid_score__c) AS Score__c, '
            + 'MAX(COALESCE(NULLIF(s.Title__c, \'\'), s.FileName__c)) AS Title__c, '
            + 'MAX(s.URL__c) AS URL__c, c.Chunk__c AS Chunk__c '
            + 'FROM hybrid_search(TABLE(' + indexDmo() + '), '
            + toSqlLiteral(cleanQuestion) + ', \'\', ' + CANDIDATE_COUNT + ', '
            + toSqlLiteral(RELEVANCE_CONFIG) + ') h '
            + 'JOIN ' + chunkDmo() + ' c ON h.SourceRecordId__c = c.RecordId__c '
            + 'JOIN ' + sourceDmo() + ' s ON c.SourceRecordId__c = s.ExternalSourceId__c '
            + buildChunkFilter()
            + 'GROUP BY c.Chunk__c '
            + 'ORDER BY MAX(h.hybrid_score__c) DESC '
            + 'LIMIT ' + MAX_PASSAGES;
    }

    @TestVisible
    private static String indexDmo() {
        return settingValue(setting?.Index_DMO__c, DEFAULT_INDEX_DMO, DMO_NAME);
    }

    @TestVisible
    private static String chunkDmo() {
        return settingValue(setting?.Chunk_DMO__c, DEFAULT_CHUNK_DMO, DMO_NAME);
    }

    @TestVisible
    private static String sourceDmo() {
        return settingValue(setting?.Source_DMO__c, DEFAULT_SOURCE_DMO, DMO_NAME);
    }

    @TestVisible
    private static String dataSpace() {
        return settingValue(setting?.Data_Space__c, DEFAULT_DATA_SPACE, DATA_SPACE_NAME);
    }

    /**
     * Returns the setting value, or the default when there is no setting record. A value that isn't
     * a plain API name throws, so the search fails safely instead of running altered SQL.
     */
    private static String settingValue(String value, String defaultValue, Pattern allowedName) {
        if (setting == null) {
            return defaultValue;
        }
        String name = value?.trim();
        if (String.isBlank(name) || !allowedName.matcher(name).matches()) {
            throw new SettingException('Invalid value in Acme_Retriever_Setting__mdt.' + SETTING_RECORD + ': ' + value);
        }
        return name;
    }

    /**
     * Builds the WHERE clause that drops page chrome, boilerplate, and very short chunks.
     */
    private static String buildChunkFilter() {
        String filter = 'WHERE LENGTH(c.Chunk__c) >= ' + MIN_CHUNK_LENGTH + ' ';
        for (String pattern : EXCLUDED_CHUNK_PATTERNS) {
            filter += 'AND c.Chunk__c NOT LIKE ' + toSqlLiteral(pattern) + ' ';
        }
        return filter;
    }

    /**
     * Normalises the question: removes control characters, collapses whitespace, and caps length.
     */
    @TestVisible
    private static String cleanQuestion(String question) {
        if (String.isBlank(question)) {
            return '';
        }
        String cleaned = question.replaceAll('[\\p{Cntrl}]', ' ').normalizeSpace();
        return cleaned.left(MAX_QUESTION_LENGTH);
    }

    /**
     * Wraps a value as a SQL string literal, doubling single quotes.
     */
    private static String toSqlLiteral(String value) {
        return '\'' + value.replace('\'', '\'\'') + '\'';
    }

    private static String unescape(String value) {
        return String.isBlank(value) ? '' : value.unescapeHtml4().trim();
    }

    /**
     * Removes email addresses, so they never reach the agent's answer.
     */
    @TestVisible
    private static String removeEmails(String text) {
        return String.isBlank(text) ? text : text.replaceAll(EMAIL_PATTERN, '').trim();
    }

    /**
     * Crawled chunks keep site-relative links such as "Read More (/en/products/x/)".
     * Prefix the site root so the LLM can hand visitors working URLs.
     */
    @TestVisible
    private static String absolutizeLinks(String text) {
        return String.isBlank(text) ? text : text.replace('(/', '(' + SITE_ROOT + '/');
    }

    /**
     * Formats passages as numbered excerpts with title and source URL on their own lines,
     * so the prompt can cite the URL.
     */
    @TestVisible
    private static String formatPassages(List<Passage> passages) {
        List<String> blocks = new List<String>();
        for (Integer i = 0; i < passages.size(); i++) {
            Passage passage = passages[i];
            List<String> lines = new List<String>{ 'Excerpt ' + (i + 1) };
            if (String.isNotBlank(passage.title)) {
                lines.add('Title: ' + passage.title);
            }
            if (String.isNotBlank(passage.url)) {
                lines.add('URL: ' + passage.url);
            }
            lines.add('Text: ' + passage.text);
            blocks.add(String.join(lines, '\n'));
        }
        return String.join(blocks, '\n\n');
    }

    @TestVisible
    private class SettingException extends Exception {}

    @TestVisible
    private class Passage {
        public String title;
        public String url;
        public String text;
    }

    /**
     * Prompt template input. The field name must match the template input API name.
     */
    public class Request {
        @InvocableVariable(label='Question' description='The website visitor question' required=true)
        public String Question;
    }

    /**
     * Prompt template output. Prompt Builder reads the single member named Prompt.
     */
    public class Response {
        @InvocableVariable(label='Prompt' description='Grounding text from the example.com website')
        public String Prompt;
    }
}
```
