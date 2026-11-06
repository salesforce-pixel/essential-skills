---
name: calling-prompt-templates-apex
description: "Call Salesforce Prompt Templates from Apex using ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate. Use this skill whenever you need to invoke an Einstein/Agentforce Prompt Template from server-side Apex — from an @AuraEnabled LWC controller, an @InvocableMethod for Flow, a service/queueable, or a trigger-adjacent handler. TRIGGER when: user mentions generateMessagesForPromptTemplate, EinsteinPromptTemplateGenerationsInput, WrappedValue, 'call a prompt template from Apex', 'invoke GenAI from Apex', resolving Flex/Field Generation/Sales Email/Record Summary prompt templates programmatically, or passing record IDs / free text into a prompt template. DO NOT TRIGGER when: authoring the Prompt Template metadata itself, building an Agentforce agent (.agent), or generating generic Apex unrelated to prompt templates."
metadata:
  version: "1.0"
---

<!--
Changelog
1.0 — Imported into essential-skills (2026-11-06) from the personal
      ~/.claude/skills copy. Doc sources tracked by tools/doc-refresh.
-->

# Calling Prompt Templates from Apex

Use this skill to invoke a Salesforce **Prompt Template** from Apex via
`ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate(devName, input)` and consume the
generated text. The pattern is identical regardless of template type — only the **input
parameter shape** changes.

This skill abstracts the boilerplate seen across hand-written implementations into one reusable
service (`assets/PromptTemplateService.cls`) plus thin entry-point examples (LWC controller,
Invocable for Flow). Prefer the service; copy the inline pattern only for one-off scripts.

## Required Inputs

Gather or infer before writing code:

- **Prompt Template developer name** (or the template record ID, `0hf…`). API name, not label.
- **Input variable name(s)** defined on the template — the part after `Input:` (e.g. `Account`,
  `accountId`, `Image`, `Contact`). Case-sensitive; must match the template exactly.
- **Input variable type(s)** — each is either a **record** (sObject reference) or a **primitive**
  (free text / id string). This determines the `WrappedValue` shape (see below).
- **Entry point** — `@AuraEnabled` LWC controller, `@InvocableMethod` (Flow/Agent action),
  service called from a Queueable, etc.
- **Org prerequisites** — Einstein Generative AI enabled; running user has the **Prompt Template
  User** permission (object `Execute Prompt Templates`). Otherwise the call throws.

If the request is clear and complete, generate immediately — don't over-ask.

---

## The 5-Step Pattern

Every invocation follows the same five steps. The reusable service does steps 1–4 for you.

```apex
// 1. Create the input wrapper
ConnectApi.EinsteinPromptTemplateGenerationsInput input =
    new ConnectApi.EinsteinPromptTemplateGenerationsInput();
input.isPreview = false; // false = resolve template AND call the LLM. true = resolve only, no LLM.

// 2. Bind input parameters — key is 'Input:' + the template's input variable name
Map<String, ConnectApi.WrappedValue> params = new Map<String, ConnectApi.WrappedValue>();
ConnectApi.WrappedValue account = new ConnectApi.WrappedValue();
account.value = new Map<String, String>{ 'id' => recordId }; // record reference
params.put('Input:Account', account);
input.inputParams = params;

// 3. Set additional config — applicationName is REQUIRED
input.additionalConfig = new ConnectApi.EinsteinLlmAdditionalConfigInput();
input.additionalConfig.applicationName = 'PromptTemplateGenerationsInvocable';

// 4. Call the service ('Draft_With_Einstein' = template dev name, or a 0hf… id)
ConnectApi.EinsteinPromptTemplateGenerationsRepresentation result =
    ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate('Draft_With_Einstein', input);

// 5. Consume the response (always guard before indexing)
String text = (result?.generations != null && !result.generations.isEmpty())
    ? result.generations[0].text : null;
```

---

## Binding Input Parameters (the part that trips people up)

The key in `inputParams` is **always** `'Input:'` + the input variable's API name as defined on
the template. The *value* shape depends on the variable type:

| Template input variable type | `WrappedValue.value` should be | Example |
|---|---|---|
| **Record / sObject** (Account, Case, Contact, ContentVersion…) | `Map<String,String>{ 'id' => recordId }` | `wv.value = new Map<String,String>{'id'=>caseId};` |
| **Primitive** (Text, Id string, Number, Boolean) | the raw value directly | `wv.value = accountId;` / `wv.value = 'Summarize in 3 bullets';` |

Notes:
- Wrong variable name, wrong `Input:` prefix, or wrong value shape → empty/blank generation or a
  thrown `ConnectApi` exception. Verify the names against the template metadata.
- A template can take **multiple** inputs — add one `params.put(...)` per variable (e.g. a Sales
  Email template often needs `Input:Recipient` and `Input:Sender`).
- For a **record** input you only need the `id`; the platform hydrates the record server-side.

---

## Optional Configuration

Set these on the input only when the requirement calls for it (defaults are fine otherwise):

- **`input.outputLanguage`** — ISO 639-1 code (`'es'`, `'fr'`, `'ja'`) to force the response
  language. See `references/api-reference.md` for the supported-language note.
- **`input.citationMode`** — `'post_generation'` or `'off'` (for grounded/Flex templates).
- **Hyperparameters** on `additionalConfig`: `temperature` (0.0–1.0), `maxTokens`,
  `numGenerations`, `frequencyPenalty`, `presencePenalty`, `stopSequences`, `enablePiiMasking`.
- **`input.isPreview = true`** — resolves the merged prompt text *without* calling the LLM. Useful
  for debugging what gets sent: read `result.prompt`. Set back to `false` to actually generate.

---

## Consuming the Response

`ConnectApi.EinsteinPromptTemplateGenerationsRepresentation` key fields:

- **`generations`** — `List<EinsteinLLMGenerationItemOutput>`; `generations[0].text` is the answer.
- **`prompt`** — the resolved template text (the merged prompt actually sent).
- **`generationErrors`** — list of errors; check it when `generations` is empty.
- `responseId` / `requestId` — for logging and traceability.

Always null-check and bounds-check before `generations[0]` — a safety block or error can leave it
empty.

---

## Governor & Platform Considerations

- The call behaves like an external callout: **it counts toward callout limits and cannot run after
  uncommitted DML in the same transaction.** Don't call it from a trigger directly — use a
  Queueable/async or invoke from a controller/Flow.
- It can be slow (LLM latency). Avoid in tight loops; **never** put it inside a `for` loop over
  bulk records without batching/async.
- Wrap every call in try/catch. Surface `e.getMessage()`; common failures are missing permission,
  unknown template dev name, and bad input variable names.
- Runs in the context of the running user — respects their Prompt Template permission.

---

## Workflow

1. **Confirm inputs** — template dev name, each input variable name + type, entry point.
2. **Reuse the service** — copy `assets/PromptTemplateService.cls` into the project if no
   equivalent exists. It centralizes steps 1–4 and the error handling.
3. **Write the entry point** — pick the matching asset:
   - LWC-invoked → `assets/PromptTemplateController.cls` (`@AuraEnabled`).
   - Flow / Agent action → `assets/PromptTemplateInvocable.cls` (`@InvocableMethod`).
   - Async/bulk → call the service from a Queueable.
4. **Set `applicationName`** on `additionalConfig` (required) and bind every input variable.
5. **Guard the response** — null/bounds check `generations`, check `generationErrors`.
6. **Deploy & test** — see `assets/PromptTemplateServiceTest.cls` for the `HttpCalloutMock`-style
   / mock-result testing approach (the ConnectApi call can't be made live in tests; isolate it).
7. **Verify** in the org with a real record id before handing off.

For the full property tables of every input/output class, read `references/api-reference.md`.

## Reference File Index

| File | When to read |
|------|-------------|
| `references/api-reference.md` | Full property tables for the input/output ConnectApi classes, method signatures, and the official Salesforce doc URLs. |
| `assets/PromptTemplateService.cls` | The reusable service — drop into any project; abstracts the 5-step pattern. |
| `assets/PromptTemplateController.cls` | `@AuraEnabled` controller example for calling a template from LWC. |
| `assets/PromptTemplateInvocable.cls` | `@InvocableMethod` example for calling a template from Flow / as an Agent action. |
| `assets/PromptTemplateServiceTest.cls` | Test class pattern for code that wraps the ConnectApi call. |
