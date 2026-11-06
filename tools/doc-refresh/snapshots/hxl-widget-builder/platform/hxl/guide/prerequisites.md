# Prerequisites

Before you build with the Headless Experience Layer (HXL), set up your development environment and enable HXL in your org. Complete these prerequisites to create and deploy HXL widgets.

## Enable HXL in Your Org

HXL is available as a beta feature in API version 67.0 and later. To use HXL widgets in your org, enable the HXL beta feature.

1. From Setup, in the Quick Find box, enter `Headless Experience Layer Settings`, and then select **Headless Experience Layer Settings**.
2. Review the beta terms. To turn on the feature, select the feature toggle.

## Set Up a Salesforce DX Project

HXL widgets are source-based metadata that you develop locally and deploy to your org. Set up a Salesforce DX (SFDX) project and connect it to your Salesforce org.

- **Install the Salesforce CLI.** Use the `sf project` commands to deploy, retrieve, and track source files. See [Install Salesforce CLI](https://developer.salesforce.com/docs/atlas.en-us.sfdx_setup.meta/sfdx_setup/sfdx_setup_install_cli.htm).
- **Create or open an SFDX project.** Store your widget bundles in the `uiWidgets` folder in your project's package directory.
- **Authorize your org.** Connect the CLI to your target org so that you can deploy and retrieve metadata. See [Authorization](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_auth.htm).

## Choose How to Build Your Widgets

You can compose and preview HXL widgets in the [HXL Playground](/docs/platform/hxl/guide/playground.md). Describe your UI as declarative JSON, preview it natively across surfaces, and copy the resulting widget definitions into your project. The playground is the fastest way to learn HXL concepts and prototype widgets.

Alternatively, vibe code your widgets in an AI-assisted development environment. Agentforce Vibes provides tooling to generate and refine widgets with AI assistance. To set up this environment, see [Get Started with Agentforce Vibes](https://developer.salesforce.com/docs/platform/agentforcevibes/guide/afv-get-started.md).

## Next Steps

After you complete these prerequisites, you're ready to build.

- Learn key concepts in [Build Rich UI Experiences with HXL Widgets](/docs/platform/hxl/guide/hxl-rich-ui.md).
- Experiment with widgets in the [HXL Playground](/docs/platform/hxl/guide/playground.md).
- Choose a target channel, either [Agentforce](/docs/platform/hxl/guide/agentforce-action-output.md) or [MCP-based channels](/docs/platform/hxl/guide/hxl-mcp-channels.md), such as Claude and Slackbot.
