/**
 * Example @AuraEnabled controller that calls a Prompt Template from an LWC.
 *
 * The LWC imports this method and renders `text`. Keep the controller thin —
 * all the ConnectApi boilerplate lives in PromptTemplateService.
 *
 * LWC call:
 *   import generate from '@salesforce/apex/PromptTemplateController.generateForRecord';
 *   const text = await generate({ recordId: this.recordId });
 */
public with sharing class PromptTemplateController {

    @AuraEnabled(cacheable=false)
    public static String generateForRecord(Id recordId) {
        // 'Input:accountId' here is a RECORD input named "accountId" on the template.
        // Swap withRecord/withValue and the variable name to match your template.
        PromptTemplateService.Result result = PromptTemplateService
            .builder('Tech_Product_Recommendation')   // <-- your template dev name
            .withRecord('accountId', recordId)         // <-- your input variable name
            .generateResult();

        if (!result.isSuccess) {
            // Surface a clean message to the LWC; the framework wraps this for the UI.
            throw new AuraHandledException(result.errorMessage);
        }
        return result.text;
    }
}
