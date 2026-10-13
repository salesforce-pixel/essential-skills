# v67-and-Earlier Agent Manifests (Bot / BotVersion model)

Copied from the standalone official example pages. **Don't** copy the inline
"Reference an Agent Version by Its Versioned Name" snippet in
`agent-dx-api-v67-earlier.md`: its `<types>` blocks are wrongly nested and the
XML is invalid.

Set `<version>` to your project/org version (examples use 66.0).
Replace every `*` on ApexClass / Flow / GenAiPromptTemplate with the names the
agent actually uses. Wildcards on those can cause very long deploys or timeouts.

## All agents (including legacy)

Use this first when deploying to an org that doesn't have the agent yet.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <!-- Top-level agent -->
    <types><members>*</members><name>Bot</name></types>
    <!-- Agent versions -->
    <types><members>*</members><name>BotVersion</name></types>
    <!-- Reasoning engine; maps subagents to actions -->
    <types><members>*</members><name>GenAiPlannerBundle</name></types>
    <!-- Agent Script source; harmless for legacy agents -->
    <types><members>*</members><name>AiAuthoringBundle</name></types>
    <!-- Subagents (topics) -->
    <types><members>*</members><name>GenAiPlugin</name></types>
    <!-- Actions -->
    <types><members>*</members><name>GenAiFunction</name></types>
    <!-- Narrow these three to named members -->
    <types><members>*</members><name>GenAiPromptTemplate</name></types>
    <types><members>*</members><name>ApexClass</name></types>
    <types><members>*</members><name>Flow</name></types>
    <version>66.0</version>
</Package>
```

## Single agent version (bundle number = committed number)

Version 2 of `NGA_Service_Agent`. The full agent must already be deployed to the target.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types><members>NGA_Service_Agent.v2</members><name>BotVersion</name></types>
    <types><members>NGA_Service_Agent_v2</members><name>GenAiPlannerBundle</name></types>
    <types><members>NGA_Service_Agent_2</members><name>AiAuthoringBundle</name></types>
    <types><members>*</members><name>GenAiPlugin</name></types>
    <types><members>*</members><name>GenAiFunction</name></types>
    <types><members>CaseEmail</members><name>ApexClass</name></types>
    <types>
        <members>Field_Generation_Flow</members>
        <members>Sales_Email_Flow</members>
        <name>Flow</name>
    </types>
    <version>66.0</version>
</Package>
```

## Single version where bundle number ≠ committed number

Saved version 9 of `TestAgentFromSource` → its `bundle-meta.xml` `<target>` is
`TestAgentFromSource.v7`, so BotVersion and GenAiPlannerBundle use 7.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types><members>TestAgentFromSource.v7</members><name>BotVersion</name></types>
    <types><members>TestAgentFromSource_v7</members><name>GenAiPlannerBundle</name></types>
    <types><members>TestAgentFromSource_9</members><name>AiAuthoringBundle</name></types>
    <types><members>*</members><name>GenAiPlugin</name></types>
    <types><members>*</members><name>GenAiFunction</name></types>
    <types><members>CaseEmail</members><name>ApexClass</name></types>
    <types>
        <members>Field_Generation_Flow</members>
        <members>Sales_Email_Flow</members>
        <name>Flow</name>
    </types>
    <version>66.0</version>
</Package>
```

## Worked example: Quick_Agentforce_Service_Agent ("Casey"), active v3

Under API 66 the latest bundle is **unsuffixed**. Its `<target>` is `.v3`:

```xml
<types><members>Quick_Agentforce_Service_Agent.v3</members><name>BotVersion</name></types>
<types><members>Quick_Agentforce_Service_Agent_v3</members><name>GenAiPlannerBundle</name></types>
<types><members>Quick_Agentforce_Service_Agent</members><name>AiAuthoringBundle</name></types>
```
