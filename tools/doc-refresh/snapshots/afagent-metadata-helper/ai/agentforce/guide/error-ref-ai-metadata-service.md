# AI Metadata Service Errors

The AI Metadata Service stores the per-org AI configuration that Agentforce uses when processing requests, including model settings, trust configuration, and agent customizations. Errors from this service typically indicate that a requested configuration record wasn't found, that a write conflicted with a concurrent update, or that a dependent service experienced a temporary failure.

## ADMIN_SERVICE_CLIENT_ERROR

A Data 360 service that the AI Metadata Service depends on rejected your request. Your request wasn't processed.

This error occurs when:

- The request contained data the service considered invalid.
- The request didn't meet the service's validation requirements.

### How to Troubleshoot

To resolve this error:

1. Review the error details for information about what was rejected.
2. Check whether your request data is valid and complete for this operation.
3. Correct the request before resubmitting.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `ADMIN_SERVICE_CLIENT_ERROR`
- What you were trying to do when the error occurred

## ADMIN_SERVICE_SERVER_ERROR

A Data 360 service that the AI Metadata Service depends on encountered an internal error. This is usually temporary.

This error occurs when:

- The service experienced an internal failure or outage.
- The service was temporarily overloaded or unreachable.

### How to Troubleshoot

To resolve this error:

1. Wait at least 5 seconds, then try again.
2. If the error persists, wait a few minutes before trying again.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `ADMIN_SERVICE_SERVER_ERROR`
- What you were trying to do when the error occurred

## CDP_MDS_CLIENT_ERROR

A Data 360 service that the AI Metadata Service depends on rejected your request. Your request wasn't processed.

This error occurs when:

- The request contained data the service considered invalid.
- The request didn't meet the service's validation requirements.

### How to Troubleshoot

To resolve this error:

1. Review the error details for information about what was rejected.
2. Check whether your request data is valid and complete for this operation.
3. Correct the request before resubmitting.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `CDP_MDS_CLIENT_ERROR`
- What you were trying to do when the error occurred

## CDP_MDS_SERVER_ERROR

A Data 360 service that the AI Metadata Service depends on encountered an internal error. This is usually temporary.

This error occurs when:

- The service experienced an internal failure or outage.
- The service was temporarily overloaded or unreachable.

### How to Troubleshoot

To resolve this error:

1. Wait at least 5 seconds, then try again.
2. If the error persists, wait a few minutes before trying again.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `CDP_MDS_SERVER_ERROR`
- What you were trying to do when the error occurred

## DOWNSTREAM_CLIENT_ERROR

A service that the AI Metadata Service depends on rejected your request. Your request wasn't processed.

This error occurs when:

- The request contained data the service considered invalid.
- The request didn't meet the service's validation requirements.

### How to Troubleshoot

To resolve this error:

1. Review the error details for information about what was rejected.
2. Check whether your request data is valid and complete for this operation.
3. Correct the request before resubmitting.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `DOWNSTREAM_CLIENT_ERROR`
- What you were trying to do when the error occurred

## DOWNSTREAM_SERVER_ERROR

A service that the AI Metadata Service depends on encountered an internal error. This is usually temporary.

This error occurs when:

- The service experienced an internal failure or outage.
- The service was temporarily overloaded or unreachable.

### How to Troubleshoot

To resolve this error:

1. Wait at least 5 seconds, then try again.
2. If the error persists, wait a few minutes before trying again.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `DOWNSTREAM_SERVER_ERROR`
- What you were trying to do when the error occurred

## ENTITY_CONFLICT_CONCURRENT_WRITE

Your request conflicted with a change that happened at the same time. The AI Metadata Service rejected your change to avoid overwriting the other update.

This error occurs when:

- Multiple clients or processes wrote to the same record at the same time.
- A previous failed request overlapped with a new one.

### How to Troubleshoot

To resolve this error:

1. Wait a few seconds, then try again.
2. After the request succeeds, confirm that your change was applied correctly.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `ENTITY_CONFLICT_CONCURRENT_WRITE`
- What you were trying to do when the error occurred

## ENTITY_CONFLICT_CONSTRAINT

Your request can't be completed because it conflicts with an existing record or a uniqueness rule. Your change wasn't saved.

This error occurs when:

- A record with the same unique value already exists.
- The request references a related record in a way that isn't allowed.

### How to Troubleshoot

To resolve this error:

1. Check whether a record with the conflicting value already exists. If it does, update the existing record instead of creating a new one.
2. Choose a different value for the field that must be unique.
3. Resubmit the request once the conflict is resolved.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `ENTITY_CONFLICT_CONSTRAINT`
- What you were trying to do when the error occurred

## ENTITY_CONFLICT_STALE_WRITE

The record you tried to update was changed by another request after you read it. The AI Metadata Service rejected your update to avoid overwriting the newer change.

This error occurs when:

- Another client or process updated the same record between your read and your write.
- Your update was based on a cached or outdated version of the record.

### How to Troubleshoot

To resolve this error:

1. Look up the current version of the record.
2. Reapply your change to the latest version.
3. Resubmit the request.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `ENTITY_CONFLICT_STALE_WRITE`
- What you were trying to do when the error occurred

## ENTITY_NOT_FOUND

The record referenced in your request doesn't exist in the AI Metadata Service. Your request wasn't processed.

This error occurs when:

- The ID in your request is incorrect or was mistyped.
- The record was deleted before this request was made.
- The record belongs to a different org than the one the request is scoped to.

### How to Troubleshoot

To resolve this error:

1. Confirm the ID in your request is correct.
2. Verify the record hasn't been deleted.
3. Resubmit the request with a valid record reference.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `ENTITY_NOT_FOUND`
- What you were trying to do when the error occurred

## INTERNAL_TRANSACTION_FAILURE

The AI Metadata Service encountered an internal error while processing your request. Your request wasn't processed. This is usually temporary.

This error occurs when:

- The service's database was temporarily unavailable or under heavy load.
- A brief infrastructure issue prevented the operation from completing.

### How to Troubleshoot

To resolve this error:

1. Wait at least 5 seconds, then try again.
2. If the error persists, wait a few minutes before trying again.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `INTERNAL_TRANSACTION_FAILURE`
- What you were trying to do when the error occurred

## INTERNAL_UNEXPECTED

The AI Metadata Service encountered an unexpected internal error while processing your request. Your request wasn't processed. This may be temporary.

This error occurs when:

- An unforeseen condition in the request or service state triggered a failure.
- The service encountered an error that doesn't match a more specific error code.

### How to Troubleshoot

To resolve this error:

1. Wait at least 5 seconds, then try again.
2. If the error persists, wait a few minutes before trying again.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `INTERNAL_UNEXPECTED`
- Whether you're able to reproduce the error

## INVALID_QUERY_FILTER

The query filter in your request is malformed, so the AI Metadata Service couldn't parse it. Your request wasn't processed.

This error occurs when:

- The filter parameter isn't valid JSON.
- The filter uses an operator or field name the service doesn't support.
- The filter's structure doesn't match what this operation expects.

### How to Troubleshoot

To resolve this error:

1. Confirm the filter parameter is well-formed JSON.
2. Verify the field names and operators are supported by this operation.
3. Resubmit the request with a corrected filter.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `INVALID_QUERY_FILTER`
- What you were trying to do when the error occurred

## INVALID_REQUEST_ARGUMENT

Your request contained a value that the AI Metadata Service couldn't accept. Your request wasn't processed.

This error occurs when:

- A required field was missing from the request.
- A field contained a value of the wrong type or an out-of-range value.
- An identifier in the request was malformed.

### How to Troubleshoot

To resolve this error:

1. Check the API documentation for the operation you called.
2. Correct the invalid argument and resubmit the request.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `INVALID_REQUEST_ARGUMENT`
- What you were trying to do when the error occurred

## METHOD_NOT_ALLOWED

The request type isn't supported for this operation. Your request wasn't processed.

This error occurs when:

- This operation doesn't support the request type used (such as DELETE).
- A typo caused the wrong request type to be sent.
- The request type was valid in a previous version of this operation but is no longer supported.

### How to Troubleshoot

To resolve this error:

1. Check the API documentation for which request types this operation supports.
2. Resubmit the request using a supported request type.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `METHOD_NOT_ALLOWED`
- What you were trying to do when the error occurred

## NOT_ACCEPTABLE

The AI Metadata Service can't respond in the format your request specified. Your request wasn't processed.

This error occurs when:

- The `Accept` header in your request specifies a format this operation doesn't support.
- A client library sets a default `Accept` header that doesn't match the formats this operation supports.

### How to Troubleshoot

To resolve this error:

1. Check the API documentation for the response formats this operation supports.
2. Update the `Accept` header to a supported format, typically `application/json`.
3. Resubmit the request.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `NOT_ACCEPTABLE`
- What you were trying to do when the error occurred

## TENANT_DATASOURCE_UNAVAILABLE

The data store for your org's AI configuration isn't available yet. This typically happens while your org is still being set up. Your request wasn't processed.

This error occurs when:

- Your org's data store is still being provisioned after initial setup.
- Infrastructure supporting your org's configuration hasn't finished coming online.

### How to Troubleshoot

To resolve this error:

1. Wait about 5 minutes, then try again.
2. If the error persists well beyond the initial setup window, your org's provisioning may be stuck.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `TENANT_DATASOURCE_UNAVAILABLE`
- What you were trying to do when the error occurred

## TENANT_NOT_READY

Your org's AI configuration isn't ready to serve requests yet. This typically happens shortly after your org is set up, while configuration is still completing in the background.

This error occurs when:

- Your org was set up recently and provisioning hasn't finished.
- A configuration update or migration for your org is in progress.

### How to Troubleshoot

To resolve this error:

1. Wait about 5 minutes, then try again.
2. If the error persists well beyond the expected setup window, provisioning may be stuck.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `TENANT_NOT_READY`
- What you were trying to do when the error occurred

## UNSUPPORTED_MEDIA_TYPE

The content type of your request isn't supported by this operation. Your request wasn't processed.

This error occurs when:

- The `Content-Type` header specifies a format this operation doesn't accept.
- The `Content-Type` header is missing or incorrect.
- The request body format doesn't match the declared content type.

### How to Troubleshoot

To resolve this error:

1. Set the `Content-Type` header to a supported format, typically `application/json`.
2. Confirm the request body matches the declared content type.
3. Resubmit the request.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `UNSUPPORTED_MEDIA_TYPE`
- What you were trying to do when the error occurred

## VALIDATION_FAILED

Your request failed the AI Metadata Service's input validation. Your request wasn't processed.

This error occurs when:

- A field or parameter didn't meet the service's validation requirements.
- A field exceeded a length or format restriction.
- A combination of parameters was inconsistent or contradictory.

### How to Troubleshoot

To resolve this error:

1. Review the request parameters against the API documentation for the operation you called.
2. Correct the invalid field and resubmit the request.

If the issue persists, contact Salesforce Customer Support with the following information.

- The trace ID from the error response (`instance` field, format `urn:trace:...`)
- The error code: `VALIDATION_FAILED`
- What you were trying to do when the error occurred
