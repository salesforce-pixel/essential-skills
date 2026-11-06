# Template: Flight search with custom input and output UI

A deployable version of the docs' Flight example
([worked-examples.md](../references/worked-examples.md#example-1-flight-search-top-level-editor--top-level-renderer)).
It has two Apex-based custom Lightning types, one for input and one for output, each with the
LWC behind it. Both are configured for Employee agents (`lightningDesktopGenAi`) and Service
agents on Enhanced Chat v2 (`enhancedWebChat`).

| Path | What |
|---|---|
| `force-app/main/default/classes/FlightAgent.cls` | `@InvocableMethod` "Find Flights" + invocable request/response wrappers |
| `classes/AvailableFlight.cls`, `Flight.cls`, `FlightRequestFilter.cls` | Top-level, `global`, `@JsonAccess` classes behind the types |
| `classes/FlightAgentTest.cls` | Covers the action (needed for production deploys) |
| `lightningTypes/flightResponse/` | Output CLT → `c/flightDetails` renderer |
| `lightningTypes/flightFilter/` | Input CLT → `c/flightRequestFilter` editor |
| `lwc/flightDetails/` | Renderer: `lightning__AgentforceOutput`, reads `value.flights`, adds `getFormattedValue()` for the copy button |
| `lwc/flightRequestFilter/` | Editor: `lightning__AgentforceInput`, `readOnly`, dispatches `valuechange` |
| `package.xml` | Manifest for all of the above (API 64.0) |

## Use it

1. Copy `force-app/` into your DX project, or rename the classes, types and LWCs first. If you
   rename, keep these in sync: the folder name ↔ `c__<name>` in the js-meta `sourceType`/`targetType`
   and in Agent Script, the `definition` ↔ the LWC folder, and `@apexClassType/c__<Class>` ↔ the class name.
2. Validate, then deploy:
   ```bash
   python3 -I <skill>/scripts/validate_clt.py force-app
   sf project deploy start --dry-run --source-dir force-app --target-org <alias>
   sf project deploy start --source-dir force-app --target-org <alias>
   ```
3. Create the agent action from **Find Flights** (Reference Action Type: Apex). If you created it
   before deploying these classes, delete it and create it again.
4. Wire it up. Either set **Input Rendering** on `filters` = `flightFilter` and **Output Rendering**
   on `aFlight` = `flightResponse`, or in Agent Script set
   `complex_data_type_name: "c__flightFilter"` / `"c__flightResponse"` and `is_displayable: True`
   on `aFlight`. The full block is in
   [apex-and-actions.md](../references/apex-and-actions.md#agent-script).
5. Preview "Find flights", check the form and the cards, then Commit and Activate.

Mobile: copy a channel folder to `lightningMobileGenAi/`. Don't need Service agents? Delete the
`enhancedWebChat/` folders.
