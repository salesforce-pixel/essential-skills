# ConnectApi.EinsteinLLM Prompt Template — API Reference

Captured from the official Salesforce Apex Reference (API v258.0). Source URLs at the bottom.

## Method: `EinsteinLLM.generateMessagesForPromptTemplate`

Generates a response using the specified prompt template and input parameters. Static. **API v60.0+.**

```apex
public static ConnectApi.EinsteinPromptTemplateGenerationsRepresentation
generateMessagesForPromptTemplate(
    String promptTemplateDevName,                                  // dev name OR record id (0hf…)
    ConnectApi.EinsteinPromptTemplateGenerationsInput promptTemplateGenerationsInput)
```

- **`promptTemplateDevName`** — Developer name **or** ID of a prompt template record.
- **`promptTemplateGenerationsInput`** — input (see below).
- **Returns** `EinsteinPromptTemplateGenerationsRepresentation`.

Related: `EinsteinLLM.getPromptTemplates(query, sortBy, offset, pageLimit, fields, type,
relatedEntity, isActive)` (API v62.0+) returns a filtered list of prompt templates. Requires the
**Execute Prompt Templates** user permission.

---

## Input: `ConnectApi.EinsteinPromptTemplateGenerationsInput`

Prompt template input parameters to use for generation.

| Property | Type | Description | Req? | Ver |
|---|---|---|---|---|
| `additionalConfig` | `EinsteinLlmAdditionalConfigInput` | Configuration for the LLM provider. | **Required** | 60.0 |
| `inputParams` | `Map<String, ConnectApi.WrappedValue>` | Parameters/values to resolve the template. Keys are `Input:<varName>`. | **Required** | 60.0 |
| `isPreview` | `Boolean` | `false` = resolve template **and** generate LLM response. `true` = resolve only (no LLM). | **Required** | 60.0 |
| `citationMode` | `String` | `post_generation` (citations after response) or `off`. | Optional | 62.0 |
| `outputLanguage` | `String` | Language code for the generated response (e.g. `en`, `es`, `fr`). | Optional | 61.0 |
| `tags` | `ConnectApi.WrappedValue` | Map of wrapped values (e.g. free-form feedback) used to resolve the template. | Optional | 62.0 |

---

## Input: `ConnectApi.EinsteinLlmAdditionalConfigInput`

Additional configuration for the LLM provider.

| Property | Type | Description | Req? | Ver |
|---|---|---|---|---|
| `applicationName` | `String` | Name of the application. Commonly `'PromptTemplateGenerationsInvocable'`. | **Required** | 60.0 |
| `additionalParameters` | `Map<String, ConnectApi.WrappedValue>` | Extra parameters/values for the LLM provider. | Optional | 60.0 |
| `enablePiiMasking` | `Boolean` | Mask personally identifiable information (`true`) or not. | Optional | 60.0 |
| `frequencyPenalty` | `Double` | Reduce repetitiveness, proportional to prior frequency. 0.0–1.0. | Optional | 60.0 |
| `presencePenalty` | `Double` | Reduce repetitiveness, applied equally to all seen tokens. 0.0–1.0. | Optional | 60.0 |
| `maxTokens` | `Integer` | Maximum number of tokens to generate. | Optional | 60.0 |
| `numGenerations` | `Integer` | Number of generation requests to send to the provider. | Optional | 60.0 |
| `stopSequences` | `List<String>` | Generation is cut at the earliest occurrence of a stop sequence. | Optional | 60.0 |
| `temperature` | `Double` | Sampling temperature. Higher = more random. 0.0–1.0. | Optional | 60.0 |

---

## Input: `ConnectApi.WrappedValue`

Wrapper used for each input parameter value. Set the `value` property:

- **Record reference:** `wv.value = new Map<String,String>{ 'id' => recordId };`
- **Primitive (text/id/number/bool):** `wv.value = accountId;` or `wv.value = 'some free text';`

---

## Output: `ConnectApi.EinsteinPromptTemplateGenerationsRepresentation`

Generated response and resolved prompt template text.

| Property | Type | Description | Ver |
|---|---|---|---|
| `generations` | `List<EinsteinLLMGenerationItemOutput>` | Generated responses. `generations[0].text` is the answer. | 60.0 |
| `prompt` | `String` | Resolved template text (merged prompt actually sent). | 60.0 |
| `generationErrors` | `List<EinsteinPromptTemplateGenerationsError>` | Errors, if any. Check when `generations` is empty. | 60.0 |
| `promptTemplateDevName` | `String` | Dev name or ID of the template record. | 60.0 |
| `parameters` | `ConnectApi.WrappedMapObject` | Parameters/values for the LLM provider. | 60.0 |
| `requestId` | `String` | ID of the generation request sent to the provider. | 60.0 |
| `citations` | `EinsteinLlmGenerationCitationOutput` | Source info for grounded responses. | 62.0 |
| `fileData` | `List<EinsteinPromptTemplateAttachment>` | File data of input files used in generation. | 63.0 |
| `isSummarized` | `Boolean` | Whether the response contains summarized text. | 61.0 |
| `requestMessages` / `responseMessages` | `List<EinsteinPromptTemplateMaskContent>` | Resolved prompts / responses with masking info. | 61.0 |
| `slotsMaskingInformation` | `List<EinsteinPromptTemplateMaskData>` | Original/placeholder values of masked data. | 61.0 |

### Output item: `ConnectApi.EinsteinLLMGenerationItemOutput`

| Property | Type | Description | Ver |
|---|---|---|---|
| `text` | `String` | **Text of the generated response.** | 60.0 |
| `responseId` | `String` | ID of the generated response. | 60.0 |
| `parameters` | `String` | Parameter values for the LLM provider. | 60.0 |
| `contentQualityRepresentation` | `EinsteinLlmGenerationsContentQuality` | Whether the response contains toxic language. | 61.0 |
| `safetyScoreRepresentation` | `EinsteinLlmGenerationSafetyScoreOutput` | Safety score info. | 60.0 |

---

## Official Source URLs

- EinsteinLLM Class (methods): https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_ConnectAPI_EinsteinLLM_static_methods.htm
- EinsteinPromptTemplateGenerationsInput: https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_connectapi_input_einstein_prompt_template_generations.htm
- EinsteinLlmAdditionalConfigInput: https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_connectapi_input_einstein_llm_additional_config.htm
- EinsteinPromptTemplateGenerationsRepresentation (output): https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_connectapi_output_einstein_prompt_template_generations.htm
