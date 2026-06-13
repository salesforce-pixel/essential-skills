# Scenario Templates

Reusable demo "stories" that turn the skill from a record generator into a demo accelerator. Each template is a starting point — always reconcile field names and picklist values against the actual org via schema-discovery.md, since orgs customize heavily.

A template defines: the object spine, the narrative, and the value ranges. Adapt counts to the demo.

## Sales — healthy pipeline (industry-agnostic)
- **Spine:** Account → Contact (2–4 each) → Opportunity (3–6 each) → OpportunityContactRole.
- **Narrative:** a quarter with a believable funnel — more early-stage than late, a couple of recent wins, one slipped deal.
- **Values:** StageName skewed to funnel shape; Amount varied $25k–$500k; open CloseDates across the next 1–3 quarters; 1–2 Closed Won in the recent past.

## Service — case load trending down
- **Spine:** Account → Contact → Case (+ optionally Tasks/Emails on cases).
- **Narrative:** volume of new cases recently lower than 60–90 days ago; mix of Open/Escalated/Closed; priorities weighted to Medium.
- **Values:** CreatedDate spread over 90 days with a downward trend; recent activities so timelines look live.

## Energy / field service (fits Equinor, Energy World, North Sea demo orgs)
- **Spine:** Account (operators/sites) → Asset/WorkOrder (if Field Service installed) → Contact (engineers) → Case.
- **Narrative:** operational sites with maintenance work orders and a few active incidents.
- **Values:** site names with real-sounding geography (North Sea, Aberdeen, Stavanger); near-term scheduled work; mix of preventive/corrective.

## Financial services (if FSC installed)
- **Spine:** Account (households/individuals) → FinancialAccount → Opportunity (referrals) → Contact.
- **Narrative:** a wealth-management book with referrals in progress.
- **Note:** FSC objects/record types vary by edition — describe first.

## How to apply a template
1. Confirm which objects actually exist and their record types (schema-discovery.md).
2. Map template fields to the org's real API names and picklist values.
3. Set counts to the demo size.
4. Generate with relative dates (generating-data.md), tag everything, dry-run, then execute.

Templates are guidance, not fixed schemas — the org is the source of truth.
