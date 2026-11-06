# Set Up Authentication for Lightning Out 2.0 | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=platform.lightning_out_auth.htm&type=5

EXTEND SALESFORCE WITH CLICKS, NOT CODE
Set Up Authentication for Lightning Out 2.0

For an external app to access components in a Lightning Out 2.0 app, the end user must be authenticated in Salesforce. The external app must also be authorized to access Salesforce resources. To set up authentication and authorization, implement an OAuth 2.0 flow and configure an External Client App (ECA) in your org. Then configure your external app to either call the Lightning Out 2.0 UI Bridge endpoint or the standard Salesforce UI Bridge endpoint. The call generates a frontdoor URL at run time, which is used to establish a Salesforce session for the Lightning Out 2.0 app.

REQUIRED EDITIONS
Available in: Lightning Experience

Available in: Professional, Enterprise, Performance, Unlimited, all Agentforce 1 Editions, and Developer Editions

USER PERMISSIONS NEEDED
To create local External Client Apps: Create, edit, and delete External Client Apps
To configure External Client Apps OAuth settings: Create, edit, and delete External Client Apps
To modify CORS settings: Modify All Data AND Customize Application
To create and modify a Lightning Out 2.0 app: Customize Application

Before you begin, complete the steps in Prepare to Build a Lightning Out 2.0 App.

Design and implement a supported OAuth 2.0 authorization flow.
IMPORTANT Lightning Out 2.0 supports OAuth 2.0 flows that provide a web-scoped access token with user context, including the web server flow and the JSON Web Token (JWT) bearer flow. The client credentials flow isn’t supported because it doesn’t provide user context, so Salesforce filters out the web scope from its access token.
In your org, create an external client app (ECA) with OAuth enabled.
Use these instructions to get set up: Create an External Client App and Configure the External Client App OAuth Settings.
In your ECA, use these OAuth settings.
Include the Manage user data via Web browsers (web) or the Full access (full) OAuth scopes.
If your ECA uses the JWT bearer flow, also include the Perform requests at any time (refresh_token) scope.
If your ECA uses one of the listed flows in the Flow Enablement section, enable and configure the settings for that flow.
Remember that Lightning Out 2.0 doesn’t support the client credentials flow.
In the Security section, you can keep these default settings selected: Require secret for Web Server Flow, Require secret for Refresh Token Flow, and Require Proof Key for Code Exchange (PKCE) extension for Supported Authorization Flows.
Lightning Out 2.0 also supports refresh token rotation and JWT-based access tokens.
To obtain a frontdoor URL at run time, call a UI Bridge API endpoint from your external app by using one of these methods.

Obtain a frontdoor URL from the Lightning Out 2.0 endpoint.

This method provides only access to Lightning Out 2.0 resources. It requires almost no extra setup and provides built-in Cross-Origin Resource Sharing (CORS) protection. To use this method, you must add your external app domain name to the Salesforce CORS allowlist. See Prepare to Build a Lightning Out 2.0 App.

Obtain a frontdoor URL from the standard UI Bridge API endpoint.

This method requires you to configure ‌your own server-side authorization flow for your external app. However, this method allows for more fine-grained control if your company has specific security requirements.

Obtain a Frontdoor URL from the Lightning Out 2.0 Endpoint

The Lightning Out 2.0 servlet extends the UI Bridge API by providing CORS support and restricts Salesforce resource access to only Lightning Out 2.0 apps.

Instead of the standard UI Bridge API endpoint services/oauth2/singleaccess, the Lightning Out 2.0 servlet uses the special endpoint services/oauth2/lightningoutsingleaccess. This endpoint directs to a Lightning Web Runtime app that sets a valid Salesforce session ID (SID) as a cookie. The SID is sent with all future requests to the org, so the user doesn’t need to reauthenticate while using the Lightning Out 2.0 app.

IMPORTANT Before you make a request to the Lightning Out 2.0 UI Bridge API endpoint, make sure that your Lightning Out 2.0 app is enabled from the Lightning Out 2.0 App Manager. See Build a Lightning Out 2.0 App.

To generate a frontdoor URL, from your external app, send a POST request to the https://MyDomainName.my.salesforce.com/services/oauth2/lightningoutsingleaccess endpoint. Include your Lightning Out 2.0 app ID and the OAuth 2.0 access token as request body parameters.

REQUEST BODY PARAMETER DESCRIPTION
lightning_out_app_id

Required. The Lightning Out 2.0 app ID.

You can find this ID on the Lightning Out 2.0 App Manager page for the app.

This ID corresponds to the value of the app-id attribute on the lightning-out-application web component. For more information about the Lightning Out 2.0 app component, see Understand Lightning Out 2.0 Architecture in the Lightning Web Components Developer Guide.

access_token

Required. The valid OAuth 2.0 access token from the user’s initial session.

It can be an opaque access token or a JSON Web Token (JWT)-based access token. The access token must have the web or full scope. Specify scopes in the external client app settings for the app that issued the access token.

The user associated with the access token can’t have the API Only User permission.

Here’s an example POST request that uses cURL.

curl -X POST \
'https://MyDomainName.my.salesforce.com/services/oauth2/lightningoutsingleaccess' \
--form 'access_token="access-token-value"' \
--form 'lightning_out_app_id="app-id"'

Here’s another example POST request that uses JavaScript. Make sure that the Content-Type header is declared as application/x-www-form-urlencoded.

fetch(
"https://MyDomainName.my.salesforce.com/services/oauth2/lightningoutsingleaccess",
{
method: "POST",
headers: {
"Content-Type": "application/x-www-form-urlencoded"
},
body: "access_token=access-token-value&lightning_out_app_id=app-id"
}
)
.then((response) => {
console.log("Status:", response.status);
return response.json();
})
.then((data) => {
console.log("Success:", data);
})
.catch((error) => {
console.error("Error:", error);
});

If successful, the UI Bridge API returns a JSON response with the frontdoor URL.

HTTP/1.1 200 OK

Content-Type: application/json
Cache-Control: no-cache,must-revalidate,max-age=0,no-store,private
....

{"frontdoor_uri":"https://MyDomainName.my.salesforce.com/secur/frontdoor.jsp?otp=otp_value"}

If unsuccessful, the API returns an error message. For error message descriptions, see Generate a Frontdoor URL to Bridge into UI Sessions.

When the frontdoor URL is returned, set the frontdoor-url attribute on the lightning-out-application component to the frontdoor_uri value. Make sure that the frontdoor-url attribute value is a string of only the URL, not the entire JSON response.

TIP To review what HTML elements comprise a Lighting Out 2.0 app, including the lightning-out-application component definition, see Understand Lightning Out 2.0 Architecture.

After the frontdoor-url attribute is set, a Lightning Web Runtime app loads and sets a valid Salesforce session ID. Your Lightning Out 2.0 app now loads on the external host page.

Obtain a Frontdoor URL from the Standard UI Bridge API Endpoint

Instead of using the Lightning Out 2.0 UI Bridge API endpoint, you can obtain a frontdoor URL from the standard UI Bridge API endpoint services/oauth2/singleaccess. This method requires you to configure ‌your own server-side authorization flow for your external app. However, this method allows for more fine-grained control if your company has specific security requirements.

NOTE Unlike the Lightning Out 2.0 endpoint, the standard UI Bridge API endpoint doesn’t support CORS settings configured in Salesforce Setup.

For instructions, see Generate a Frontdoor URL to Bridge into UI Sessions. In your request, don’t include the redirect_uri parameter. Instead of being taken to the Salesforce homepage, users see the Lightning Out 2.0 app components on the external host page.

When the frontdoor URL is returned, set the frontdoor-url attribute on the lightning-out-application component to the frontdoor_uri value. Make sure that the frontdoor-url attribute value is a string of only the URL, not the entire JSON response.

After the frontdoor-url attribute is set, a Lightning Web Runtime app loads and sets a valid Salesforce session ID. Your Lightning Out 2.0 app now loads on the external host page.

SEE ALSO
External Client Apps
Authorize Apps with OAuth
Generate a Frontdoor URL to Bridge into UI Sessions
Lightning Web Components Developer Guide: Understand Lightning Out 2.0 Architecture
