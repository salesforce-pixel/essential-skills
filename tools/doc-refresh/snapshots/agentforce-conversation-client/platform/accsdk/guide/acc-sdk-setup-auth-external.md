# Set Up External Client Apps

External client apps (ECA) are a new generation of connected apps. ECAs provide single sign-on (SSO) and use OAuth protocols to authorize external apps. The external apps that are integrated with Salesforce can run on the customer success platform and other platforms, devices, or SaaS subscriptions.

For more information on ECAs, including how to configure them in your organization, see [External Client Apps](https://help.salesforce.com/s/articleView?id=xcloud.external_client_apps.htm).

ACC uses Lightning Out 2.0 to embed the LWC-based conversational client into external, third-party web applications that run outside the Salesforce domain. Because these applications operate outside the Salesforce trust boundary, they require a secure way to authenticate and interact with Salesforce services.

An External Client App (ECA) provides this capability by enabling OAuth 2.0–based authentication and authorization. With an ECA, the embedded ACC client securely accesses Salesforce APIs and user context from outside Salesforce. See [Set Up Authentication for Lightning Out 2.0](https://help.salesforce.com/s/articleView?id=platform.lightning_out_auth.htm\&type=5).

1. To create an ECA for your ‌organization, from the Salesforce Setup page, enter *External* in the Quick Find box, and then select **External Client App Manager**.

2. Click **New External Client App**.

3. Enter the basic information

   - Enter the name for the ECA to display in the External Client App Manager.
   - Enter the API name to be used when referring to your app from a program. This field defaults to a version of the app’s name with underscores in place of the spaces.
   - Enter the contact email for Salesforce to use in case we want to contact you or your support team.
   - Determine the distribution state. To develop an app for your local org, choose **Local**. To develop an app for packaging and distribution, choose **Packaged**.

4. Click **Enable OAuth** to configure the OAuth policy.

5. Enter the app settings.

   - Enter the **Callback URL**. The callback URL is the app URL where you’re embedding the code and the URL can accept the authentication returned from the Salesforce ECA. An example of a callback URL is https\://<3p-domain>/callback.html.
   - For **OAUTH Scopes**, select Manage user data via APIs (api), Manage user data via Web browsers (web), and Access Lightning applications (lightning). If you have other OAuth needs, select other scopes as needed.

6. For Flow Enablement, select the appropriate flow for your web app.

   - If you select **Enable Authorization Code and Credentials Flow**, specify if user credentials are required in the POST body.
   - If you select **Client Credentials Flow**, it only works with the Manage user data via APIs (api), Access Lightning applications (lightning), or Manage user data via Web browsers(web) OAuth Scopes.

7. For Security, select **Require secret for Refresh Token** and any other options you need.

8. Click **Create**.

If you are generating an access token, on the Settings tab, click **Consumer Key and Secret** to copy and save the values. You need the consumer key value for the client_id and the consumer secret value for the client_secret.

## Additional JWT Bearer Flow Settings

To use the JWT Bearer authentication flow, after you create your ECA, you must follow these steps.

#### Update the OAuth Policies for your ECA.

1. In Salesforce Setup, enter External in the Quick Find box, and then select External Client App Manager.
2. To edit your ECA, select it from the list of apps.
3. Click Edit.
4. In the OAuth Policies section, update the Permitted Users value to Admin approved users are pre authorized.
   ![](https://a.sfdcstatic.com/developer-website/sfdocs/agentforce-conversation-client/media/manage-external-client-apps.png)
5. In the App Policies section, add the custom permission set to the Selected Permission Sets list.
   ![](https://a.sfdcstatic.com/developer-website/sfdocs/agentforce-conversation-client/media/app-policies.png)
6. Save and close.

***

#### See Also

[Setup Trusted Domains](/docs/platform/accsdk/guide/acc-sdk-setup-trusted-domains.md)
