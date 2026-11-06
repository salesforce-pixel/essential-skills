## Generate the Access Token for Agentforce Conversation Client Web SDK

To complete the authentication process, you need to generate an access token and a `frontdoor` URL. Use the generated `frontdoor` URL as the `authCredential` value when you initialize the SDK.

## Generate the Access Token

To generate the token without creating logic for single sign-on, you can use this command to get the access_token. In this command, the location references your Salesforce org and `client_id` and `client_secret` are the values that you copied and saved from the OAuth Settings.

```
curl --location 'https://<your-salesforce-org>/services/oauth2/token' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode 'client_id=<client_id_of_the_app_created_in_previous_step>' \
--data-urlencode 'client_secret=<client_secret_of_the_app_created_in_previous_step>'
```

For more information on Salesforce OAuth flows and access tokens, see

- [User-Agent OAuth Authentication Flow](https://developer.salesforce.com/docs/atlas.en-us.chatterapi.meta/chatterapi/intro_oauth_user_agent_flow.htm)
- [OAuth 2.0 User-Agent Flow](https://developer.salesforce.com/docs/platform/mobile-sdk/guide/oauth-useragent-flow.md)
- [Portal Authentication Using OAuth 2.0 and Salesforce Site](https://developer.salesforce.com/docs/platform/mobile-sdk/guide/oauth-portal-force-com-sites.md)

## Generate a Frontdoor URL for Embedding

Frontdoor URLs are used to bridge into UI sessions, giving users uninterrupted access to Salesforce and other apps. It uses an existing session to automatically log users into a new UI with making them enter their credentials again.

:::note
Frontdoor URLs are short-lived. For session refresh, a new frontdoor URL must be generated.
:::

### Example: Generate a Frontdoor URL in JavaScript

```
const getFrontdoorUrl = async (accessToken: string, instanceUrl: string) => {
  try {
    const frontdoorEndpoint = `${instanceUrl}/services/oauth2/singleaccess`;

    const myHeaders = new Headers();
    myHeaders.append('accept', 'application/json');
    myHeaders.append('authorization', `Bearer ${accessToken}`);
    myHeaders.append('content-type', 'application/x-www-form-urlencoded');

    const urlencoded = new URLSearchParams();

    const requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: urlencoded
    };

    const response = await fetch(frontdoorEndpoint, requestOptions);
    if (!response.ok) {
      return {error: `Salesforce API responded with ${response.status}`, statusCode: response.status};
    }
    const responseData = await response.json();
    return {frontdoorUrl: responseData.frontdoor_uri};
  } catch (error) {
    // eslint-disable-next-line no-console
    console.error('Error in getFrontdoorUrl:', error);
    return {error: error.message || 'Failed to generate frontdoor URL'};
  }
};
```

For information on how to use the UI Bridge API to generate frontdoor URLs, see [Generate a frontdoor URL to Bridge into UI Sessions](https://help.salesforce.com/s/articleView?id=xcloud.frontdoor_singleaccess.htm\&type=5).

## Authentication Management

- Don't hardcode OAuth tokens or frontdoor URLs in your client-side code.
- Pass credentials to the browser only when strictly necessary. Credentials can be scrapped from the browser by malicious actors.

***

#### See Also

[Get Your Employee Agent ID](/docs/platform/accsdk/guide/acc-sdk-get-acc-agent-id.md)
