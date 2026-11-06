# Apex classes, schema projection, and wiring the type to the action

## Apex class requirements (Apex-based CLTs)

These matter most in namespaced orgs and managed packages, but apply them everywhere.

| Rule | Detail |
|---|---|
| **Top-level** | Define every class the type references as a top-level class in its own file. No inner classes |
| **`global`** | `public`/`private` can fail in namespaced orgs and packages |
| **`@JsonAccess`** | `@JsonAccess(serializable='always' deserializable='always')` on **every** class, so the invocation layer can (de)serialize it |
| **`@AuraEnabled`** | On every field the response needs, including fields inside objects used as `@InvocableVariable`. Schema projection only exposes `@AuraEnabled` members |
| **Namespace** | `c__` for local classes. The package namespace only for classes from another managed package |

**Supported field types:** primitives (Integer, Double, Long, Date, Datetime, Time, String, ID,
Boolean), generic or specific sObjects (`Account`, `MyObject__c`), lists/arrays of any of these
(including user-defined classes and nested collections), `Map<String, V>` (key is always a String,
V is a primitive, sObject or collection), and user-defined Apex classes.

> If you created the agent action **before** the classes met these rules, **delete and recreate
> the action** after you fix the Apex. Editing it doesn't register the change.

The docs' examples break some of these rules:
- `FlightAgent` uses **inner** `FlightRequest`/`FlightResponse` wrapper classes. They're the
  invocable method's request/response, not the class behind `lightning:type`. Only the referenced
  classes (`AvailableFlight`, `Flight`, `FlightRequestFilter`) are top-level.
- The Hotel example annotates fields with `@InvocableVariable` only (no `@AuraEnabled`). Put
  **both** on fields in classes the CLT projects from.

## Pattern: invocable wrapper → CLT-backed class

```apex
global class FlightAgent {
    @InvocableMethod(label='Find Flights' description='Finds available flights')
    global static List<FlightResponse> findFlights(List<FlightRequest> req) { ... }

    @JsonAccess(serializable='always' deserializable='always')
    global class FlightRequest {
        @InvocableVariable global String originCity;
        @InvocableVariable global Date dateOfTravel;
        @InvocableVariable global FlightRequestFilter filters;   // ← input CLT (editor)
    }
    @JsonAccess(serializable='always' deserializable='always')
    global class FlightResponse {
        @InvocableVariable global AvailableFlight aFlight;       // ← output CLT (renderer)
    }
}

@JsonAccess(serializable='always' deserializable='always')
global class AvailableFlight {            // own file
    @AuraEnabled global List<Flight> flights;
}
```

The action parameter carries the class type (`@apexClassType/c__AvailableFlight`). The CLT's
`schema.json` points at the **same** class. Then the parameter's rendering is switched to the CLT.

## Schema projection

- The LightningTypeBundle API reads the referenced class and exposes every `@AuraEnabled` member.
- It converts Apex primitives and complex types (nested classes, sObjects) into Lightning type
  schemas automatically, so you don't map fields by hand.
- The class is the single source of truth. Change the class and the type's structure follows,
  with no `schema.json` edit. Only **additive** changes are safe
  (see [bundle-and-schema.md](bundle-and-schema.md#safe-changes)).

## Wire the type to the agent action

### Agentforce Builder / Setup

1. Open the agent action (Agentforce Builder, or Setup → Agentforce Assets → Actions).
2. **Output:** on the output parameter, turn on *Show in conversation* and set **Output
   Rendering** to your CLT.
   **Input:** on the input parameter, set **Input Rendering** to your CLT.
3. Save. Reload the agent or the Builder preview.

### Agent Script

Doc pattern: create the action from the Apex method, switch to **Script** mode, and replace the
parameter's `complex_data_type_name` with the CLT name:

```agentscript
    actions:
        Find_Flights:
            label: "Find Flights"
            description: "find available flights"
            target: "apex://FlightAgent"
            inputs:
                filters: object
                    label: "filters"
                    is_required: True
                    is_user_input: True
                    complex_data_type_name: "c__flightFilter"        # was "@apexClassType/c__FlightRequestFilter"
                    description: "filters"
                dateOfTravel: object
                    label: "dateOfTravel"
                    is_required: True
                    is_user_input: True
                    complex_data_type_name: "lightning__dateType"
                    description: "date info"
            outputs:
                aFlight: object
                    label: "aFlight"
                    complex_data_type_name: "c__flightResponse"      # was "@apexClassType/c__AvailableFlight"
                    is_displayable: True
                    filter_from_agent: False
                    description: "result"
```

- List output: `hotels: list[object]` with `complex_data_type_name: "c__hotelResponse"` (the
  type's renderer.json has the `collection` override).
- `is_displayable: True` is **required** to show an output that uses a CLT.
- `is_user_input: True` marks inputs the user provides, so the agent collects them instead of
  inferring them.
- CLT names use the `c__` prefix plus the **folder name**, not the `title`. Script validation fails
  if the type doesn't exist in the org, so deploy the bundle first.
- Route to the subagent from the router, e.g.
  `go_to_Flight_Search: @utils.transition to @subagent.Flight_Search`. Identifiers are case-sensitive.
- In reasoning, reference the action with `{!@actions.Find_Flights}` and leave inputs as slots:
  `with filters = ...`.
- The LLM sometimes asks for input as text. Write the subagent instructions so it uses the action
  (and so the form): "use {!@actions.Find_Flights} … collect … before running the action".

For full Agent Script syntax, see [`agentscript`](../../agentscript/SKILL.md).

## Test → commit → activate

Builder **Preview**: send an utterance such as "Find flights". Check that the custom form appears,
submit it, and check that the custom card renders. Then **Commit Version** → **Commit**, then
**Activate**. Activating deactivates the previous active version. After a commit, further edits
need a new draft.

## Citations from Apex actions

Apex actions can return citations to Employee agents and through the Agent API. The agent must be
activated. Platform-generated citations only work for agents **created after May 26, 2025**.
Sources are unstructured: knowledge articles, PDFs, web pages.

| Class | Use when |
|---|---|
| `AiCopilot.GenAiCitationInput` | You give the reasoning engine **sources**, and it decides where to place citations (calls the citations platform) |
| `AiCopilot.GenAiCitationOutput` | Your action returns **explicit citations** from its own logic and skips the reasoning engine |

Both have a customizable `label`. Make sure end users can open the source URL and label.

Pattern (`GenAiCitationInput` from a prompt template with a retriever):

```apex
// Call the template with citations turned on
ConnectApi.WrappedValue question = new ConnectApi.WrappedValue();
question.value = query;
ConnectApi.EinsteinPromptTemplateGenerationsInput req = new ConnectApi.EinsteinPromptTemplateGenerationsInput();
req.additionalConfig = new ConnectApi.EinsteinLlmAdditionalConfigInput();
req.additionalConfig.applicationName = 'PromptBuilderPreview';
req.isPreview = true;                      // doc sample; false = run the template for real
req.citationMode = 'post_generation';
req.inputParams = new Map<String, ConnectApi.WrappedValue>{ 'Input:Question' => question };  // = template input API name
ConnectApi.EinsteinPromptTemplateGenerationsRepresentation out =
    ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate('Knowledge_Search', req);

// Convert ConnectApi citations → AiCopilot
AiCopilot.GenAiSourceReference ref = new AiCopilot.GenAiSourceReference(null,
    new List<AiCopilot.GenAiSourceContentInfo>{ new AiCopilot.GenAiSourceContentInfo(fieldName, objectName, content) },
    new List<AiCopilot.GenAiSourceReferenceInfo>{ new AiCopilot.GenAiSourceReferenceInfo(link, recordId, objectApiName) });
AiCopilot.GenAiCitationInput sources = new AiCopilot.GenAiCitationInput(null, new List<AiCopilot.GenAiSourceReference>{ ref });

// Invocable response
public class Response {
    @InvocableVariable(required=true description='Generated text response from the LLM') public String Data;
    @InvocableVariable(required=true description='Structured citation sources') public AiCopilot.GenAiCitationInput sources;
}
```

Read the source lists from `out.citations.sourceReferences[*].contents` / `.metadata`, and null-check
`out.citations`. The docs set `response.Data = output.prompt`. For a generated answer you usually
want `output.generations[0].text`, so check which one your template returns. To call a prompt
template from Apex in general, see `calling-prompt-templates-apex`.
