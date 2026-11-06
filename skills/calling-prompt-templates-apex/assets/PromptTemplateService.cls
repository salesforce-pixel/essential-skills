/**
 * Reusable service for invoking Salesforce Prompt Templates from Apex via
 * ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate.
 *
 * Centralizes the 5-step pattern (build input -> bind params -> set config -> call -> read)
 * so callers (controllers, invocables, queueables) stay thin.
 *
 * Usage — record input:
 *   String text = PromptTemplateService.builder('Business_Card_Scanner_Prompt')
 *       .withRecord('Image', fileId)
 *       .generate();
 *
 * Usage — primitive input + language + multiple params:
 *   PromptTemplateService.Result r = PromptTemplateService.builder('Tech_Product_Recommendation')
 *       .withValue('accountId', accountId)
 *       .outputLanguage('es')
 *       .generateResult();
 *   if (r.isSuccess) { System.debug(r.text); } else { System.debug(r.errorMessage); }
 */
public with sharing class PromptTemplateService {

    /** Default application name expected by the generations service. */
    @TestVisible
    private static final String DEFAULT_APP_NAME = 'PromptTemplateGenerationsInvocable';

    /** Simple result wrapper so callers don't catch exceptions everywhere. */
    public class Result {
        public Boolean isSuccess;
        public String text;          // generations[0].text
        public String resolvedPrompt; // result.prompt (merged template text)
        public String errorMessage;
    }

    /** Fluent builder. Create via PromptTemplateService.builder(devName). */
    public class Builder {
        private final String templateDevName;
        private final Map<String, ConnectApi.WrappedValue> params =
            new Map<String, ConnectApi.WrappedValue>();
        private final ConnectApi.EinsteinPromptTemplateGenerationsInput input =
            new ConnectApi.EinsteinPromptTemplateGenerationsInput();
        private final ConnectApi.EinsteinLlmAdditionalConfigInput config =
            new ConnectApi.EinsteinLlmAdditionalConfigInput();

        private Builder(String templateDevName) {
            this.templateDevName = templateDevName;
            this.input.isPreview = false;
            this.config.applicationName = DEFAULT_APP_NAME;
        }

        /** Bind a record/sObject input variable (value is a record Id). */
        public Builder withRecord(String inputVarName, Id recordId) {
            ConnectApi.WrappedValue wv = new ConnectApi.WrappedValue();
            wv.value = new Map<String, String>{ 'id' => recordId };
            params.put('Input:' + inputVarName, wv);
            return this;
        }

        /** Bind a primitive input variable (text, id-as-string, number, boolean). */
        public Builder withValue(String inputVarName, Object value) {
            ConnectApi.WrappedValue wv = new ConnectApi.WrappedValue();
            wv.value = value;
            params.put('Input:' + inputVarName, wv);
            return this;
        }

        /** Force the LLM response language (ISO 639-1, e.g. 'es', 'fr', 'ja'). */
        public Builder outputLanguage(String isoCode) {
            if (String.isNotBlank(isoCode)) {
                input.outputLanguage = isoCode;
            }
            return this;
        }

        /** Override the application name if your org requires a different one. */
        public Builder applicationName(String appName) {
            config.applicationName = appName;
            return this;
        }

        /** Optional sampling temperature (0.0 - 1.0). */
        public Builder temperature(Double value) {
            config.temperature = value;
            return this;
        }

        /** Optional max tokens for the generation. */
        public Builder maxTokens(Integer value) {
            config.maxTokens = value;
            return this;
        }

        /**
         * Resolve the template only (no LLM call). After generate(), read the
         * resolvedPrompt on the Result to inspect the merged prompt.
         */
        public Builder previewOnly() {
            input.isPreview = true;
            return this;
        }

        /** Execute and return the generated text, or throw on failure. */
        public String generate() {
            Result r = generateResult();
            if (!r.isSuccess) {
                throw new PromptTemplateException(r.errorMessage);
            }
            return r.text;
        }

        /** Execute and return a Result wrapper (never throws for handled errors). */
        public Result generateResult() {
            Result r = new Result();
            try {
                input.inputParams = params;
                input.additionalConfig = config;

                ConnectApi.EinsteinPromptTemplateGenerationsRepresentation response =
                    callService(templateDevName, input);

                r.resolvedPrompt = response != null ? response.prompt : null;

                if (response != null
                        && response.generations != null
                        && !response.generations.isEmpty()) {
                    r.text = response.generations[0].text;
                    r.isSuccess = true;
                } else {
                    r.isSuccess = false;
                    r.errorMessage = buildErrorMessage(response);
                }
            } catch (Exception e) {
                r.isSuccess = false;
                r.errorMessage = e.getMessage();
                System.debug(LoggingLevel.ERROR, 'PromptTemplateService error: ' + e.getMessage());
            }
            return r;
        }
    }

    /** Entry point: PromptTemplateService.builder('My_Template_Dev_Name'). */
    public static Builder builder(String templateDevName) {
        return new Builder(templateDevName);
    }

    /**
     * Thin seam around the ConnectApi call so tests can stub it (the real call
     * cannot execute in a test context). @TestVisible lets a test set the stub.
     */
    @TestVisible
    private static ConnectApi.EinsteinPromptTemplateGenerationsRepresentation callService(
            String devName, ConnectApi.EinsteinPromptTemplateGenerationsInput input) {
        if (Test.isRunningTest() && mockResponse != null) {
            return mockResponse;
        }
        return ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate(devName, input);
    }

    /** Test hook — set this in a test to bypass the live ConnectApi call. */
    @TestVisible
    private static ConnectApi.EinsteinPromptTemplateGenerationsRepresentation mockResponse;

    private static String buildErrorMessage(
            ConnectApi.EinsteinPromptTemplateGenerationsRepresentation response) {
        if (response != null && response.generationErrors != null
                && !response.generationErrors.isEmpty()) {
            return 'Generation failed: ' + JSON.serialize(response.generationErrors);
        }
        return 'No generations returned from the prompt template.';
    }

    public class PromptTemplateException extends Exception {}
}
