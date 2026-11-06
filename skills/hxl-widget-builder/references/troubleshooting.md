# Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Widget files deploy nowhere / "no source" | Written to `force-app/uiWidgets/` | Must be `force-app/main/default/uiWidgets/<name>/` |
| `UiWidgetBundle` type unknown | API version < 67.0 | Set `sourceApiVersion` ≥ 67.0 in `sfdx-project.json` and `<version>` in package.xml |
| CLT deploy fails: widget not found | CLT deployed before widget | Deploy widget first or in the same package |
| MCP wrapper CLT fails on `c__…OutputValues` | Payload CLT missing/not deployed | Deploy payload CLT first; check spelling/case |
| Agentforce shows default (plain) output | Output Rendering not set, or agent not reloaded | Agentforce Assets → action output → Show in conversation + Output Rendering → reload agent |
| CLT not selectable in Output Rendering | CLT class ≠ output data type | CLT `@apexClassType/c__Outer$Inner` must match the output's data type |
| Widget renders empty values | Renderer key/path mismatch | Keys = widget schema names; values = CLT paths (`outputValues.<prop>.<field>` for MCP) |
| Whole list missing | `forEach` bound to wrong path, or `if` references `$attrs` (evaluates once) | Bind `{!$attrs.list}`; use loop var in per-item `if` |
| Evaluation error on `if` | Non-Boolean expression | Use a Boolean attr (explicit comparisons work in A/B only) |
| Widget deploy fails: "You can't add the `<attr>` property … `additionalProperties` keyword value is set to false" | Attribute name not valid for that component (e.g. `wrap` on `tile/row`, `url` on `tile/link`) | Use the official name (`isWrapped`, `href`); see `components.md` or `curl` the component's `.md` reference page |
| Widget deploy fails: "Schema update contains breaking changes: You can't delete …" | Removed a property from a deployed widget `schema.json` | Put it back (and its renderer mapping); stop binding it instead |
| MCP client: tool "crashed while formatting the result" and quotes a `{!…IF(…$attrs.x…)}` expression | Formula over `$attrs` in an MCP-rendered widget; the renderer only remaps plain bindings | Compute the value in Apex, add it to the widget schema + renderer, bind it plainly. `validate_hxl.py` → `mcp-plain-bindings` |
| Same crash persists after the fix is deployed, quoting the **old** expression | Client cached the old UI resource/tool list | Retrieve the org's widget to prove the fix is live, then disconnect + reconnect the connector and use a new chat. If still stale, deactivate/activate the MCP server |
| MCP client shows a markdown table with correct data, no card | Tool has no `<uiResource>`, usually because the tool was edited, removed or re-added in Setup, which wipes it | Retrieve `McpServerDefinition`, re-add `<uiResource>` (value = `<resourceName>`), redeploy, reconnect. `validate_hxl.py` → `mcp-ui-resource` |
| Can't find the Apex action when adding an MCP tool in Setup | Class not deployed yet | Deploy the Apex class first |
| Button greyed out | No `actions.click` | Add `action/openLink` or `action/sendMessage` |
| sendMessage does nothing useful | Agent lacks an action/instructions for that message | Add the follow-up action to the subagent and instruct routing |
| Image broken in Claude/ChatGPT | Auth-protected URL or domain not trusted | Public URL + Trusted URL in Setup |
| Widget not shown in MCP client, text only | `<uiResource>` ≠ `<resourceName>`, URI points to wrong CLT, server not activated, or client doesn't support MCP Apps | Fix XML, redeploy, Activate; use a supported client |
| Slack shows no widget | Block Kit path | Use standard MCP Apps path |
| Old version still renders in client | Client caches UI resource and tool list per connection | Disconnect + reconnect the connector, then a new chat (waiting doesn't help) |
| Widget edited in Setup Lightning Types breaks | Unsupported for widget-referencing CLTs | Edit in DX project, redeploy |
| Delete widget | — | `destructiveChanges.xml` with `UiWidgetBundle` member |
