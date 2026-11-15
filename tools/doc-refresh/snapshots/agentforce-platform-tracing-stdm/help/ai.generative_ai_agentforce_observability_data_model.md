# Agentforce Observability Data Model | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=ai.generative_ai_agentforce_observability_data_model.htm&type=5

QUICKSTART YOUR EINSTEIN GENERATIVE AI SOLUTION
Agentforce Observability Data Model

The Agentforce Observability data model combines Agent Analytics and Agent Optimization data with Agentforce Session Tracing. It includes session trace logs, intents, LLM calls, feedback, and Trust Layer metrics for analyzing agent performance.

REQUIRED EDITIONS
REQUIRED EDITIONS
Agentforce Observability is available in Salesforce Enterprise, Performance, and Unlimited Editions with Salesforce Foundations or Agentforce 1 Edition.
Data Model Elements

When you turn on Agentforce Observability, the system provisions a data model in Data 360 to track agent metrics, intents, evaluations, feedback, and generated content. Elements include a data stream and its target Data Lake Object (DLO), and a semantic data model (SDM) with:

Entities such as DMOs and Logical Views
Relationships that define the joins and connections among different SDM entities.
Dimensions and Measurements

This illustration shows key elements.

Data Model Entities

The following entities make up the Agentforce Observability data model. The diagram identifies the primary analytics entities, related physical DMOs, and derived logical views.

Session and identity: AI Agent Session, AI Agent Session Participant, AI Agent Session Log, Bot, Bot Version, and Session Participant Extended.
Interactions and orchestration: AI Agent Interaction, AI Agent Interaction Step, AI Agent Interaction Message, AI Agent Topic, AI Agent Action, and AI Retriever Quality Metric.
Moments and evaluations: AI Agent Moment, AI Agent Moment Interaction, AI Agent Tag, AI Agent Tag Definition, AI Agent Tag Definition Association, AI Agent Tag Association, Moment Tag Association, Moment Quality Score, Session Tag Association, and Interaction Tag Association.
Quality, feedback, and generation: AI Response Generation, AI Content Quality Category, Categorized Content Quality, AI Feedback, AI Feedback Additional Info, Gen AI Gateway Request Object Record, and Gen AI Gateway Request Object Record Content.
Voice calls: Voice Call, when the Voice Call installation succeeds and you have Service Cloud Voice or Native Voice access. Voice Call is added automatically when you enable the Session Tracing Data Model. If you don't have that access or the installation fails, Voice Call appears gray as an unmapped object in the semantic data model.
Voice Call Fields

When Voice Call is mapped, it includes Created Date, Disconnect Reason, ID, and Quality Score.

Calculated Fields

The Agentforce Observability semantic layer represents the links between session tracing, interactions, moments, evaluations, and feedback. To view the model, in Data 360, go to the semantic model tab and open Agentforce Analytics Foundations. The semantic layer provides calculated fields for querying session and agent performance data. For example, understand the relationship between session duration and quality ratings by combining `Session_Count`, and `Average_Session_Duration_clc` measures with the `Quality_Score_clc` dimension, or track weekly or monthly performance trends by combining the `Unique_Sessions_clc`, and `Abandonment_Rate_clc` measures with `Session_Date dimension`.

Customize the Data Model

The measures, dimensions, and formulas on this page describe the standard Agentforce Observability semantic data model. When these definitions don't fully represent your business process, edit the Service Agent Analytics Extension SDM or Employee Agent Analytics Extension SDM instead of rebuilding the standard model.

In an extension model, you can:

Override a standard calculated field so an existing metric reflects custom business logic. For example, include support-case creation in Escalation Status and Escalation Rate.
Add scorer outputs and use them in calculated fields and metrics.
Add synced Data 360 objects and relate them to session data. For example, connect the User object to AI Agent Session Participant to report sentiment and usage by employee.
Use the extended model in standard dashboards or build a custom dashboard.

For step-by-step Service Agent and Employee Agent examples, see Customize Agentforce Observability.

Watch Define Custom Metrics for Agentforce Agents to see both examples from the semantic model through the finished dashboards.

Calculated Field Reference

Measures are calculated numerical values that quantify agent performance. Dimensions are categorical fields for grouping, filtering, and segmenting those measures. Agent Optimization contributes intent-level fields, including duration and quality scores.

The calculated field references include each field's label, description, API name, and formula.

Agentforce Observability Measure Formulas
Agentforce Observability Dimension Formulas
Understand Quality Score
Quality Score is an out-of-the-box, LLM-based scorer in Agentforce Observability. It rates how well an agent's responses serve the user on a scale from 1, lowest, to 5, highest.
Agentforce Observability Measure Formulas
These formulas show how Agentforce Observability calculates measures in the Agentforce Analytics Foundations semantic data model. Use them to understand the metrics available for reporting.
Agentforce Observability Dimension Formulas
These formulas show how Agentforce Observability calculates dimensions in the Agentforce Analytics Foundations semantic data model. Use them to understand the fields available for reporting.
