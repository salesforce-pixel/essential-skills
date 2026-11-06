## Setup Trusted Domains

After creating your ECA, you need to update your Salesforce settings for trusted domains and use of cookies. Updating settings requires Salesforce Admin permissions.

### Update Session Setting for Trusted Domains

Add a trusted domain for the web app where you are embedding your insights.

- At the top of any Salesforce page, click the setup gear icon, then click **Setup**.\
  ![](https://a.sfdcstatic.com/developer-website/sfdocs/agentforce-conversation-client/media/setup-trusted-domains.png)
- From the Setup page, enter *Session* in the Quick Find box, and then select **Session Settings**.
- Scroll down to **Trusted Domains for Inline Frames** and click **Add Domain**.
- Enter the domain. Acceptable formats are `example.com`, `https://example.com`, and \*.example.com.
- Select **Lighting Out** for the iFrame type and save.

***

#### See Also

[Generate the Access Token for Agentforce Conversation Client Web SDK](/docs/platform/accsdk/guide/acc-sdk-setup-token.md)
