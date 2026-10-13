# v68 Agent Manifests (AiAgentDefinition model)

Use only when the source org **and** target org are both on API 68.0+.
Always retrieve with `--root-type-with-dependencies AiAgentDefinitionVersion`
so the agent's flows, Apex and prompt templates come along automatically.
Add any other metadata the agent needs (custom objects/fields, Data 360) as extra `<types>`.

**AiAuthoringBundle member name:** the CLI-generated `package.xml` (from a
`--target-metadata-dir` retrieve) lists the bundle as `<Agent>_N`, e.g.
`Quick_Agentforce_Service_Agent_3`. The doc templates below use the bare `<Agent>`.
For a deploy, prefer the generated `package.xml` (see SKILL.md Step 2A) over
hand-written manifests. `sf project deploy start` has no
`--root-type-with-dependencies`, so dependencies must already be listed.

## All versions of one agent (Agent Script)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>MyServiceAgent</members>
        <name>AiAgentDefinition</name>
    </types>
    <types>
        <members>MyServiceAgent#*</members>
        <name>AiAgentDefinitionVersion</name>
    </types>
    <types>
        <members>MyServiceAgent</members>
        <name>AiAuthoringBundle</name>
    </types>
    <version>68.0</version>
</Package>
```

## Specific versions (2 and 3)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>MyServiceAgent</members>
        <name>AiAgentDefinition</name>
    </types>
    <types>
        <members>MyServiceAgent#2</members>
        <members>MyServiceAgent#3</members>
        <name>AiAgentDefinitionVersion</name>
    </types>
    <types>
        <members>MyServiceAgent</members>
        <name>AiAuthoringBundle</name>
    </types>
    <version>68.0</version>
</Package>
```

(The official "versions 2 and 3" example omits `AiAuthoringBundle`. Keep it for Agent Script agents, as the docs' deploy rules require.)

## All agents

```xml
<types><members>*</members><name>AiAgentDefinition</name></types>
<types><members>*</members><name>AiAgentDefinitionVersion</name></types>
<types><members>*</members><name>AiAuthoringBundle</name></types>
```

## Worked example (verified retrieve, 2026-10-13)

Org `partnerBootcamp2026` (API 68.0), project `sourceApiVersion` 66.0:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types><members>Quick_Agentforce_Service_Agent</members><name>AiAgentDefinition</name></types>
    <types><members>Quick_Agentforce_Service_Agent#3</members><name>AiAgentDefinitionVersion</name></types>
    <types><members>Quick_Agentforce_Service_Agent</members><name>AiAuthoringBundle</name></types>
    <version>68.0</version>
</Package>
```

```bash
sf project retrieve start --manifest manifest/agent.xml \
  --root-type-with-dependencies AiAgentDefinitionVersion --target-org partnerBootcamp2026 --json
```

Returned: `AiAgentDefinition`, `AiAgentDefinitionVersion` `#3`, `AiAuthoringBundle`
**`Quick_Agentforce_Service_Agent_3`** (requested as the unsuffixed name), and the
dependent Flow `Quick_Agentforce_Service_Agent_Outbound_Messaging_Flow`.
