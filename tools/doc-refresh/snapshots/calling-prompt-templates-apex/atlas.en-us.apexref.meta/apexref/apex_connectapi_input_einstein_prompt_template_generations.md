# ConnectApi.​EinsteinPrompt​Template​GenerationsInput

Source: https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_connectapi_input_einstein_prompt_template_generations.htm

ConnectApi.​EinsteinPrompt​Template​GenerationsInput
 
 Prompt template input parameters to use for generation.

 
 
 
 
 
 
 
 
 
 Property 

 Type 

 Description 

 Required or Optional 

 Available Version 

 

 

 
 
 additional​Config 

 ConnectApi.​EinsteinLlm​Additional​ConfigInput 

 Configuration information for the LLM
 provider. 

 Required 

 60.0 

 

 
 citationMode 

 String 

 
 Mode of citations for the specified prompt template.
 Valid values are: 
 
 post_generation —Citations are generated
 after the generated response for the specified prompt template.

 
 off —Citations aren't generated for the
 specified prompt template.

 

 

 Optional 

 62.0 

 

 
 inputParams 

 
 Map <String, ConnectApi.WrappedValue > 

 Parameters and values to resolve the specified prompt
 template. 

 Required 

 60.0 

 

 
 isPreview 

 Boolean 

 Specifies whether to only resolve the prompt template
 ( true ) or to resolve the prompt template
 and generate an LLM response ( false ). 

 Required 

 60.0 

 

 
 outputLanguage 

 String 

 Language code for the language to generate the LLM
 response in. See Supported Languages in Prompt Template
 Responses . 

 Optional 

 61.0 

 

 
 tags 

 ConnectApi.WrappedValue 

 Map of wrapped values, such as free-form user feedback, that can
 be used to resolve a specified prompt template. 

 Optional 

 62.0
