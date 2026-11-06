# Sources and known doc inconsistencies

Built on 2026-11-06. Every URL below is tracked in `tools/doc-refresh/sources.json` under
`clt-agentforce-actions`. `/refresh-skills` re-fetches them into
`tools/doc-refresh/snapshots/clt-agentforce-actions/`, and the snapshot `git diff` shows
what changed upstream. Every developer.salesforce.com page is served as Markdown at the
`.md` URL (`curl -sL <url>`).

| # | URL | Topic | Reference file |
|---|---|---|---|
| 1 | https://developer.salesforce.com/docs/ai/agentforce/guide/lightning-types.md | CLTs for agent action UI. Apex-only limit | SKILL |
| 2 | https://developer.salesforce.com/docs/ai/agentforce/guide/lightning-types-get-started.md | Resource map | SKILL |
| 3 | https://developer.salesforce.com/docs/ai/agentforce/guide/lightning-types-standard.md | Standard types in actions. Input/Output Rendering | apex-and-actions |
| 4 | https://developer.salesforce.com/docs/ai/agentforce/guide/lightning-types-example-full-editor-renderer.md | Flight example (editor + renderer) | worked-examples, templates |
| 5 | https://developer.salesforce.com/docs/ai/agentforce/guide/lightning-types-example-collection-renderer.md | Hotel example (collection renderer) | worked-examples |
| 6 | https://developer.salesforce.com/docs/ai/agentforce/guide/global-copy.md | `getFormattedValue()` copy | ui-overrides |
| 7 | https://developer.salesforce.com/docs/ai/agentforce/guide/citations.md | Citations in Apex actions | apex-and-actions |
| 8 | https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types.md | Standard vs custom. Apex vs object categories | SKILL, bundle-and-schema |
| 9 | https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-core.md | Bundle, channels, deploy, namespaces, labels, config files | bundle-and-schema |
| 10 | https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-apex.md | Apex schema, class rules, projection, change rules | bundle-and-schema, apex-and-actions |
| 11 | https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-object.md | Object schema, layout, change rules | bundle-and-schema |
| 12 | https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-custom-editor.md | Top-level editor, attribute mapping | ui-overrides |
| 13 | https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-custom-renderer.md | Top-level renderer, attribute mapping | ui-overrides |
| 14 | https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-custom-collection-renderer.md | Collection renderer | ui-overrides |
| 15 | https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-custom-editor-property.md | Property-level editor, layout | ui-overrides |
| 16 | https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-setup.md | Setup → Lightning Types page | bundle-and-schema |
| 17 | https://developer.salesforce.com/docs/platform/api-metadata/references/meta-types/metadata-lightningtypebundle.md | Metadata API LightningTypeBundle | bundle-and-schema |
| 18 | https://github.com/forcedotcom/sf-skills/tree/main/skills/platform-custom-lightning-type-generate | sf-skills CLT generator: strict metaschema rules, errors. Tracked as raw files: `SKILL.md`, `assets/primitive-types-and-constraints.md`, `references/widget-rendition.md` | bundle-and-schema, ui-overrides, SKILL |

Linked from these pages but not captured: Lightning Type UI Configuration
(`lightning-types-ui-config`), Lightning Types Reference (`lightning-types-references`),
Agentforce Vibes skill (`lightning-types-skills`), the LWC target pages
(`targets-lightning-agentforce-input/-output`), the Connect REST Type System resources, the
Citations Apex reference, and the Help articles (`platform.lt_intro`, `sf.salesforce_app_clt_mobile`).
Add them to `sources.json` if the skill needs them.

## Known inconsistencies (docs vs docs, docs vs sf-skills)

1. **`attributes` on Apex-based types.** The renderer/editor pages (#12, #13) map
   `{!$attrs.cardName}` on an Apex class (`TaskRecord`). sf-skills (#18) says this is rejected by
   `unevaluatedProperties` because the projected schema has no `properties`. `hxl-widget-builder`
   (tested in an org) maps `$attrs` on Apex types for **widget** renderers. The skill defaults to
   no `attributes`.
2. **Object-based root keys.** The docs (#11, #15) omit `"type": "object"` and
   `"unevaluatedProperties": false`. sf-skills says the root must have both. The docs examples are
   the minimum. Add the sf-skills keys if a deploy rejects the schema.
3. **Top-level classes.** #10 says no inner classes. #4 uses inner `FlightRequest`/`FlightResponse`
   (only as invocable wrappers, not CLT-referenced). sf-skills and hxl-widget-builder use
   `@apexClassType/c__Outer$Inner`.
4. **`@AuraEnabled` vs `@InvocableVariable`.** #10 requires `@AuraEnabled` on response fields.
   #5's Hotel classes only use `@InvocableVariable`.
5. **`@JsonAccess`.** #10 says annotate every class. The #17 sample `Flight` class has none.
6. **Hotel example step 4** says "Locate the `filters` output parameter". The output is `hotels`.
7. **Hotel LWC template** quotes bindings (`"{value}"`, `"{hotel.name}"`). LWC needs `{value}`.
8. **Global copy snippet** `getFormattedValue = () {` is invalid JS. Use a method or `= () => {}`.
9. **`lightning__stringType`** appears in #3. The standard type list (#8) has `lightning__textType`
   and no string type.
10. **`lightning__listType`** is used for lists (#3, #5, sf-skills) but isn't in #8's list of
    standard types.
11. **Editor `value`.** #12 says the agent can't pre-populate `value`, but #4's filter LWC still
    reads `this.value` in `connectedCallback` (harmless, but don't rely on it).
12. **Agent Script example labels** in #4/#5 call `apexClassType` "the bundle name". It's the
    reference prefix for Apex class types. The bundle (CLT) name is the `c__<folder>` value.
