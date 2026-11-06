/**
 * Test pattern for code that wraps ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate.
 *
 * The live ConnectApi call cannot be executed in a test context, so we inject a
 * pre-built response through the @TestVisible `mockResponse` seam on the service.
 * This lets us assert the success path, the empty-generations path, and the
 * exception path without ever hitting the LLM.
 */
@IsTest
private class PromptTemplateServiceTest {

    /** Helper: build a representation with a single generation containing `text`. */
    private static ConnectApi.EinsteinPromptTemplateGenerationsRepresentation buildResponse(
            String text) {
        ConnectApi.EinsteinLLMGenerationItemOutput item =
            new ConnectApi.EinsteinLLMGenerationItemOutput();
        item.text = text;

        ConnectApi.EinsteinPromptTemplateGenerationsRepresentation resp =
            new ConnectApi.EinsteinPromptTemplateGenerationsRepresentation();
        resp.generations = new List<ConnectApi.EinsteinLLMGenerationItemOutput>{ item };
        resp.prompt = 'Resolved prompt text';
        return resp;
    }

    @IsTest
    static void generate_returnsText_onSuccess() {
        PromptTemplateService.mockResponse = buildResponse('Hello from the LLM');

        Test.startTest();
        String result = PromptTemplateService.builder('My_Template')
            .withValue('topic', 'widgets')
            .generate();
        Test.stopTest();

        System.assertEquals('Hello from the LLM', result, 'Should return generations[0].text');
    }

    @IsTest
    static void generateResult_reportsFailure_whenNoGenerations() {
        ConnectApi.EinsteinPromptTemplateGenerationsRepresentation empty =
            new ConnectApi.EinsteinPromptTemplateGenerationsRepresentation();
        empty.generations = new List<ConnectApi.EinsteinLLMGenerationItemOutput>();
        PromptTemplateService.mockResponse = empty;

        Test.startTest();
        PromptTemplateService.Result r = PromptTemplateService.builder('My_Template')
            .withRecord('Account', '001000000000000AAA')
            .generateResult();
        Test.stopTest();

        System.assertEquals(false, r.isSuccess, 'Empty generations should be a failure');
        System.assertNotEquals(null, r.errorMessage, 'Error message should be populated');
    }
}
