# Troubleshoot Custom Connections

Use this reference when your custom connection fails to deploy or the agent isn't returning properly formatted responses.

| Issue                                | Resolution                                                                                                         |
| :----------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| Invalid JSON schema                  | Verify that the `input` field in your `AiResponseFormat` contains valid, properly escaped JSON.                    |
| Missing references                   | All response formats referenced in `AiSurface` must exist as deployed `AiResponseFormat` entities.                 |
| Metadata deployment errors           | If deploying incrementally, deploy `AiResponseFormat` entities before `AiSurface` entities.                        |
| Surface type mismatch                | Ensure the `surfaceType` in `AiSurface` matches the `surfaceType` in your `plannerSurfaces` entry.                 |
| Responses are not properly formatted | Verify that your Agent API session call includes `"surfaceConfig": {"surfaceType": "Custom"}` in the request body. |

## See Also

- [Set Up a Custom Connection](/docs/ai/agentforce/guide/custom-connections-get-started.md)
- [Response Format Examples for Custom Connections](/docs/ai/agentforce/guide/custom-connections-response-formats.md)
