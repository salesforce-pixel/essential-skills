# Templates — how they map into an SFDX project

| Template path | Copy to |
|---|---|
| `widget/accountHealthCard/*` | `force-app/main/default/uiWidgets/accountHealthCard/` |
| `apex/*` | `force-app/main/default/classes/` |
| `agentforce/accountHealth/*` (scenario B) | `force-app/main/default/lightningTypes/accountHealth/` |
| `mcp/accountHealthOutputValues/*` (scenario C payload) | `force-app/main/default/lightningTypes/accountHealthOutputValues/` |
| `mcp/accountHealthResult/*` (scenario C wrapper) | `force-app/main/default/lightningTypes/accountHealthResult/` |
| `package.xml` | `manifest/package.xml` |

Rename consistently: widget folder = file stems = `@widget/c/<name>`; CLT folder = `c__<name>` references.
