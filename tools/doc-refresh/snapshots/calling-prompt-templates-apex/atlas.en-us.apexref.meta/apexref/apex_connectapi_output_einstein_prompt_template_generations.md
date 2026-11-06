# ConnectApi.​EinsteinPrompt​Template​Generations​Representation

Source: https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_connectapi_output_einstein_prompt_template_generations.htm

ConnectApi.​EinsteinPrompt​Template​Generations​Representation
 
 Generated response from the LLM provider and resolved prompt template text.

 
 
 
 
 
 
 
 
 Property Name 

 Type 

 Description 

 Available Version 

 

 

 
 
 citations 

 ConnectApi.EinsteinLlmGenerationCitationOutput 

 Source information associated with the
 generated responses. 

 62.0 

 

 
 fileData 

 
 List < ConnectApi.EinsteinPromptTemplateAttachment > 

 File data of the input files used in
 generation. 

 63.0 

 

 
 generationErrors 

 
 List < ConnectApi.EinsteinPromptTemplateGenerationsError > 

 List of errors associated with the
 generated responses, if any. 

 60.0 

 

 
 generations 

 
 List < ConnectApi.EinsteinLlmGenerationItemOutput > 

 List of generated responses from the LLM
 provider. 

 60.0 

 

 
 isSummarized 

 Boolean 

 Specifies whether the generated response
 contains summarized text (true) or not (false) . 

 61.0 

 

 
 parameters 

 ConnectApi.WrappedMapObject 

 Map of parameters and values for the LLM
 provider parameters. 

 60.0 

 

 
 mergeField​Information 

 ConnectApi.EinsteinPromptTemplateMergeFieldInformationContext 

 Merge field information mapping
 used for annotations in the resolved prompt. 

 64.0 

 

 
 prompt 

 String 

 Prompt template text with resolved
 inputs. 

 60.0 

 

 
 promptTemplate​DevName 

 String 

 Developer name or ID of the prompt
 template record. 

 60.0 

 

 
 requestId 

 String 

 ID of the generation request sent to the LLM
 provider. 

 60.0 

 

 
 renderConfiguration 

 String 

 Render configuration used for
 rendering output in embeddable prompt display
 component. 

 65.0 

 

 
 requestMessages 

 
 List < ConnectApi.​EinsteinPrompt​TemplateMask​Content​ > 

 List of resolved prompt templates with
 masked data and masking information. 

 61.0 

 

 
 responseMessages 

 
 List < ConnectApi.​EinsteinPrompt​TemplateMask​Content​ > 

 List of generated responses with masked
 data and masking information for the specified prompt
 template. 

 61.0 

 

 
 slotsMasking​Information 

 
 List < ConnectApi.​EinsteinPrompt​TemplateMaskData > 

 List of original and placeholder
 values of the masked data. 

 61.0
