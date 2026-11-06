/**
 * Example @InvocableMethod that calls a Prompt Template — usable from Flow or
 * as an Agentforce action. Generic: the template dev name, input variable name,
 * record id, and optional language are all passed in by the caller.
 *
 * Bulk-safe: processes each request; the ConnectApi call is per-request.
 */
public with sharing class PromptTemplateInvocable {

    public class Request {
        @InvocableVariable(label='Prompt Template Developer Name' required=true)
        public String templateDevName;

        @InvocableVariable(label='Input Variable Name'
            description='Template input variable, e.g. Account or accountId (no Input: prefix)'
            required=true)
        public String inputVarName;

        @InvocableVariable(label='Record Id'
            description='Record id to bind when the input variable is a record/sObject')
        public String recordId;

        @InvocableVariable(label='Text Value'
            description='Value to bind when the input variable is a primitive (text/number)')
        public String textValue;

        @InvocableVariable(label='Output Language (ISO code)'
            description='Optional, e.g. es, fr, ja')
        public String outputLanguage;
    }

    public class Response {
        @InvocableVariable(label='Generated Text')
        public String text;

        @InvocableVariable(label='Success')
        public Boolean isSuccess;

        @InvocableVariable(label='Error Message')
        public String errorMessage;
    }

    @InvocableMethod(label='Generate from Prompt Template'
        description='Resolves a Prompt Template and returns the LLM response text'
        category='Prompt Templates')
    public static List<Response> generate(List<Request> requests) {
        List<Response> responses = new List<Response>();
        for (Request req : requests) {
            PromptTemplateService.Builder builder =
                PromptTemplateService.builder(req.templateDevName)
                    .outputLanguage(req.outputLanguage);

            // Bind as a record if a recordId is given, otherwise as a primitive value.
            if (String.isNotBlank(req.recordId)) {
                builder.withRecord(req.inputVarName, (Id) req.recordId);
            } else {
                builder.withValue(req.inputVarName, req.textValue);
            }

            PromptTemplateService.Result r = builder.generateResult();

            Response resp = new Response();
            resp.text = r.text;
            resp.isSuccess = r.isSuccess;
            resp.errorMessage = r.errorMessage;
            responses.add(resp);
        }
        return responses;
    }
}
