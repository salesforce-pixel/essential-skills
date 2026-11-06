# Build with Agentic Coding Tools

You can build Multi-Framework apps with an agentic coding tool such as Claude Code, Cursor, OpenCode, or Agentforce Vibes. Salesforce doesn't tie Multi-Framework to one tool. Its agentic support builds on open standards, including the Agent Skills specification and the Model Context Protocol (MCP), so the same setup works across any tool that supports them.

Setup comes down to three pieces: the agent context that ships with your project, a library of Salesforce skills, and an MCP server that connects your tool to your org. After that, your tool follows a standard workflow to build and deploy your app. This topic explains what each piece does and how to set it up.

:::note
Keep your Salesforce CLI and Salesforce Extension Pack current so that you have the latest skills and tooling.
:::

## Understand the Agent Context in Your Project

Agentic tools read context files in your project to learn its conventions. Every generated Multi-Framework project includes an `AGENT.md` file at the project root. This file tells an agentic tool how to work in a Multi-Framework project, so any tool that reads agent-context files picks up Multi-Framework conventions automatically. You don't create or configure it.

The agent context directs your tool to:

- Run build, lint, and dev commands from inside the UIBundle directory (`<source>/uiBundles/<appName>/`), not the project root.
- Access Salesforce data through the Data SDK rather than calling `fetch` or `axios` directly.
- Leave generated files such as `schema.graphql` in place instead of editing them.
- Check for a relevant skill before starting a task, because skills are the authoritative source of guidance.

## Install the AI Skills Library

Skills are packaged, task-specific instructions that your agentic tool loads when it needs them. Salesforce publishes a library of skills for building on the platform, including a set specific to Multi-Framework and UIBundle development.

How you install the library depends on your tool:

- For Agentforce Vibes, the skills are installed and updated for you. No action is needed.
- For other tools, such as Claude Code or Cursor, run:

  ```bash
  npx skills add forcedotcom/sf-skills
  ```

The Multi-Framework skills follow the same arc as this guide. There's a skill for generating a project, one for building the frontend, one for accessing Salesforce data, ones for creating internal and external apps, and skills for deploying, localizing, and adding features such as file upload and the Agentforce conversation client. When you ask your tool to perform one of these tasks, such as generating a project or accessing Salesforce data, it loads the matching skill.

:::note
The AI skills library changes frequently and doesn't follow the same stability guarantees as generally available platform APIs. Skills can be renamed, restructured, or removed between releases. Install the library with the command above rather than depending on a fixed set of skills.
:::

## Connect Your Tool to Your Org with the MCP Server

To let your agentic tool authorize orgs, deploy and retrieve metadata, run queries, and fetch your GraphQL schema, connect it to the Salesforce DX MCP server.

You add an MCP server to your tool's configuration rather than running it directly. Where that configuration lives depends on your tool, but each tool needs the same command and arguments:

- Command: `npx`
- Arguments: `-y @salesforce/mcp --orgs DEFAULT_TARGET_ORG --toolsets orgs,metadata,data`

Most tools express this as a JSON entry:

```json
{
  "mcpServers": {
    "salesforce": {
      "command": "npx",
      "args": [
        "-y",
        "@salesforce/mcp",
        "--orgs",
        "DEFAULT_TARGET_ORG",
        "--toolsets",
        "orgs,metadata,data"
      ]
    }
  }
}
```

The toolsets most relevant to Multi-Framework development are:

- `orgs`: authorize, open, and manage orgs.
- `metadata`: deploy and retrieve metadata, including your UIBundle.
- `data`: run SOQL queries against your org.

The MCP server authorizes an org you've already connected with the Salesforce CLI. Authorize your org before you start your tool.

## How Your Tool Builds the App

With skills and the MCP server in place, your agentic tool follows the workflow defined in the project's agent context:

1. It works from the UIBundle directory and uses the project's `npm` scripts to build, lint, and run the dev server.
2. It fetches the GraphQL schema from your org with `npm run graphql:schema`, then generates typed operations from it with `npm run graphql:codegen`.
3. It accesses Salesforce data through the Data SDK. See [Access Salesforce Data and Platform Capabilities](/docs/platform/multiframework/guide/data-sdk-usage.md).
4. It deploys the UIBundle and its metadata to your authorized org through the MCP server.

## Related Salesforce Building Tools

The tools in this topic are for pro-code developers who build Multi-Framework apps in code. Salesforce also offers Builder Central (Beta), a no-code way for admins and builders to create apps and agents by describing what they want in plain language. Builder Central builds React-based apps, but through a guided, conversational flow rather than in code.

## See Also

- [Set Up Your Org for Multi-Framework App Development](/docs/platform/multiframework/guide/mfw-setup.md)
- [Quick Start: Build and Run Your First App](/docs/platform/multiframework/guide/mfw-quick-start.md)
- *AI Skills Library*: [forcedotcom/sf-skills](https://github.com/forcedotcom/sf-skills)
- *Salesforce Help*: [Get Started with Builder Central (Beta)](https://help.salesforce.com/s/articleView?id=platform.builder_central_get_started.htm\&type=5)
