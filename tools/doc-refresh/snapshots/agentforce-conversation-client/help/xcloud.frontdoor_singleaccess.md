# Generate a Frontdoor URL to Bridge into UI Sessions | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=xcloud.frontdoor_singleaccess.htm&type=5

IDENTIFY YOUR USERS AND MANAGE ACCESS
Generate a Frontdoor URL to Bridge into UI Sessions

To give users uninterrupted access to Salesforce and other apps, use an existing session to automatically log users into a new UI without making them enter their credentials again. For example, redirect users from a custom app to a specific record in Salesforce. To bridge from one session to another, use Single Access UI Bridge API (UI Bridge API for short). With this API, exchange an access token for a frontdoor URL that you use to load a new session. You can also specify a redirect URI where users are sent when their new session begins.

REQUIRED EDITIONS
Available in: all editions
How UI Bridge API Works

Think of the access token from the user’s existing session as a key and the frontdoor URL as a door that guards access to Salesforce UIs. With the access token as their key, the user can walk straight through the door into a Salesforce UI with a brand-new session.

Here are a few examples of how you can use this feature.

If you use Salesforce headless identity flows for an off-platform app, you can bridge headless app sessions into Salesforce UIs. For example, you host an ecommerce site on a headless, off-platform app that uses Salesforce headless identity flows. You also use a Salesforce Experience Cloud site to manage customer support cases. In your headless app, you want to display a button for each of a user’s active support cases so that they can jump to a specific case and view its details. To see the case details, the user must go to the Experience Cloud site. At this point, the user has already logged in to your headless app, but doesn’t have a session with the Experience Cloud site yet.

Instead of making the user log in again when they’re redirected, you can use UI Bridge API. You send the user’s access token from their headless app session to the services/oauth2/singleaccess endpoint on your Experience Cloud site. For the redirect URI, you specify a path that points to the specific Salesforce case that the user requests to see. UI Bridge API responds to this request with a frontdoor URL. The headless app redirects the user to the frontdoor URL, automatically logs them into the Experience Cloud site UI, and redirects them to their case.

Another use case is launching from an existing session in one app into an OAuth flow in a second app. For example, you’re using an Experience Cloud site as a single sign-on (SSO) provider for multiple headless and headed apps. You want to bridge a session initiated in a headless app into a headed app. You send the access token from the headless session to UI Bridge API, specifying the authorization URL of the headed app as your redirect URI. You use the resulting frontdoor URL to load a new session in the headed app. The user is logged in to the Experience Cloud SSO provider and immediately redirected to the authorization URL of the headed app. The headed app then begins an OAuth flow. At the end of this process, the user is logged into both apps with minimal disruption.

How to Use UI Bridge API

To get a frontdoor URL, send a POST or GET request to the services/oauth2/singleaccess endpoint. This endpoint supports My Domain and Experience Cloud site URLs only. Other login URLs such as login.salesforce.com and test.salesforce.com aren’t supported.

Include these parameters in the request to the services/oauth2/singleaccess endpoint.

HEADER REQUIRED? DESCRIPTION
Authorization: Bearer Required for GET requests. For GET requests, you can send the access token only in an Authorization header. For POST requests, you can send the access token in this header or in the request body.

The access token from the user’s initial session. It can be an opaque access token or a JSON Web Token (JWT)-based access token. The access token must have the web or full scope. Specify scopes in the external client app settings for the app that issued the access token.

The user associated with the access token can't have the API Only User permission.

PARAMETER REQUIRED? DESCRIPTION
access_token

For POST requests only, required in the request body only if you don’t send the access token in a header.

This parameter isn't supported for GET requests.

The access token from the user’s initial session. It can be an opaque access token or a JSON Web Token (JWT)-based access token. The access token must have the web or full scope. Specify scopes in the external client app settings for the app that issued the access token.

The user associated with the access token can't have the API Only User permission.

redirect_uri No. If you don’t include a redirect_uri, users are taken to the homepage for the My Domain or Experience Cloud site.

A relative path that points to where the user is redirected when their new session begins. You can specify any path on a Salesforce domain. For example, point users to a specific account page, object, or record.

For Experience Cloud sites, if your URL’s root path includes a suffix, include the suffix when you specify the relative path. For example, if your root URL is https://myexperiencecloudsite.com/mysitename, and you want to direct users to a page called mypage, include the site suffix mysitename in your redirect_uri so that the full value is mysitename/mypage.

Here’s an example that generates a frontdoor URL that redirects to an org’s user management page in Setup. This example is a POST request with the access token in the request body.

POST /services/oauth2/singleaccess? HTTP 1.1
Host: mydomainname.my.salesforce.com

access_token=**************&
redirect_uri=lightning/setup/ManageUsers/home

This example also generates a frontdoor URL that redirects to an org’s user management page, but it uses a GET request. For security, GET requests must send the access token in a header.

GET /services/oauth2/singleaccess? HTTP 1.1
Host: mydomainname.my.salesforce.com
Authorization: Bearer <access token>

redirect_uri=lightning/setup/ManageUsers/home

This POST example generates a frontdoor URL that redirects to a custom page called mypage in an Experience Cloud site. The Experience Cloud site’s root path includes a suffix, so the redirect URI also includes this suffix.

POST /services/oauth2/singleaccess? HTTP 1.1
Host: myexperiencecloudsite.com/mysitename

access_token=**************&
redirect_uri=mysitename/mypage
NOTE Depending on the type of Experience Cloud site and when it was created, some Experience Cloud site URLs include /s. For more information, see Custom URL Paths in LWR Sites.

If successful, the API returns a JSON response with the frontdoor URL. Here’s what the response looks like if you include a redirect_uri, which is reflected in the startURL value. If you don’t include a redirect_uri, the frontdoor URL doesn’t include a startURL.

{
"frontdoor_uri": "https://mydomainname.my.salesforce.com/secur/frontdoor.jsp?otp=*****&startURL=lightning%2Fsetup%2FManageUsers%2Fhome&cshc=x000001X7tNx0000006GpL"
}

The frontdoor URL in the response is valid for up to 1 minute from when it was returned and can be used only one time. During this time frame, if you send the same request to UI Bridge API, it returns the exact same URL. If you make multiple requests, it doesn’t extend the expiration time of this URL. The endpoint returns a new URL only when the first one has expired.

If unsuccessful, the API returns an error. Here’s an example error response.

Bad_OAuth_Token

Here’s a list of errors and suggestions for resolving them.

ERROR MESSAGE ERROR DESCRIPTION
Bad_OAuth_Token

The access token isn't valid. For example, the token expired. Try getting a new access token.

Bad_OAuth_Token is also returned if the user associated with the token has the API Only User permission. If the user requires UI access, remove this permission.

Missing_OAuth_Token We can't find an access token in the request. Include an access token in either an Authorization header (supported for GET and POST requests) or in the access_token parameter (supported only for POST requests).
Invalid_Param The redirect_uri isn’t valid. For example, it’s an absolute URL. Use a relative path only.
Invalid_Scope The access token doesn’t include either the web or full scope. Check that one of these scopes is assigned to the external client app that’s issuing the access token.
No_Access The request was sent to an invalid domain, such as login.salesforce.com or test.salesforce.com. Use a My Domain or Experience Cloud site URL only.
Wrong_Org The request was sent to a domain that’s different from the org where the access token was issued. Make sure that these values match.
