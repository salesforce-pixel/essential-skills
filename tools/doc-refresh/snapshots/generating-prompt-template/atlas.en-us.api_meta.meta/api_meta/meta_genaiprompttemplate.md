# GenAiPromptTemplate

Source: https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_genaiprompttemplate.htm

GenAiPromptTemplate
 
 Represents the definition of a prompt template, including
 its related objects and fields. 

 
 
 
 Important

 Where possible, we changed noninclusive terms to align with our company
 value of Equality. We maintained certain terms to avoid any effect on customer
 implementations.

 

 
 Parent Type

 This type extends the Metadata metadata type and inherits its
 fullName field.

 
 File Suffix and Directory Location

 
 GenAiPromptTemplate components have the suffix
 .genAiPromptTemplate and are stored in the
 genAiPromptTemplates folder.

 

 
 Version

 
 GenAiPromptTemplate components are available in API version 60.0 and later.

 

 
 Special Access Rules

 
 GenAiPromptTemplate is available only if Prompt Builder is enabled in your org and you have
 the Prompt Template Manager permission.

 

 
 Fields

 
 
 
 
 
 
 
 Field Name 

 Description 

 

 

 
 
 activeVersion 

 
 
 
 Field Type 

 int 

 
 
 Description 

 This tag will be deprecated in 63.0 and will not work in 64.0 and later. Use
 activeVersionIdentifier instead. 

 
 

 

 

 
 activeVersionIdentifier 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Specifies the version identifier of the active prompt template version. This
 tag will use versionIdentifier as the value for the active version. 

 
 

 

 
 

 
 description 

 
 
 
 Field Type 

 string 

 
 
 Description 

 A description of the prompt template. 

 
 

 

 

 
 masterLabel 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Required. A user-friendly name for GenAiPromptTemplate, which is defined
 when the GenAiPromptTemplate is created. 

 
 

 

 

 
 overridable 

 
 
 
 Field Type 

 boolean 

 
 
 Description 

 Indicates whether the prompt template can be overridden when part of a
 managed package. 

 
 

 

 

 
 relatedEntity 

 
 
 
 Field Type 

 string 

 
 
 Description 

 The Salesforce record type that the prompt template is associated with. 

 
 

 

 

 
 relatedField 

 
 
 
 Field Type 

 string 

 
 
 Description 

 The Salesforce field that the prompt template is associated with. 

 
 

 

 

 
 templateVersions 

 
 
 
 Field Type 

 
 GenAiPromptTemplateVersion [] 

 
 
 Description 

 Required. An array of prompt template versions. 

 
 

 

 

 
 type 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Required. Represents the template type that the prompt template is based on.
 Valid values are: 
 einstein_gpt__fieldCompletion 

 einstein_gpt__salesEmail 

 einstein_gpt__recordSummary 

 einstein_gpt__flex 

 einstein_gpt__caseEmailDraft 

 

 

 
 

 

 

 
 visibility 

 
 
 
 Field Type 

 GenAiPromptTemplateVisibilityType ( enumeration of type string) 

 
 
 Description 

 Indicates the scope of visibility for the prompt template. Valid values are: API 

 Global 

 

 

 
 

 

 

 

 

 

 
 GenAiPromptTemplateVersion

 
 Represents a version of a prompt template.

 
 
 
 
 
 
 Field Name 

 Description 

 

 

 
 
 content 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Required. Text of the prompt template version. 

 
 

 

 
 

 
 description 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Description of the prompt template version. 

 
 

 

 
 

 
 fileDroppingStrategy 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Defines the strategy for managing attached files when context limits are
 exceeded. 

 
 

 

 

 
 generationTemplateConfigs 

 
 
 
 Field Type 

 
 GenAiPromptTemplateGenerationConfig [] 

 
 
 Description 

 Reference to the policies for the prompt template version. 

 
 

 

 

 
 inputs 

 
 
 
 Field Type 

 
 GenAiPromptTemplateInput [] 

 
 
 Description 

 An array of prompt template inputs associated with the prompt template
 version. 

 
 

 

 
 

 
 isCitationEnabled 

 
 
 
 Field Type 

 boolean 

 
 
 Description 

 Indicates whether citations are included in generated responses. 

 
 

 

 

 
 outputSchema 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Defines the expected JSON schema structure for the generated output. 

 
 

 

 

 
 primaryModel 

 
 
 
 Field Type 

 string 

 
 
 Description 

 The model associated with the prompt template version. 

 
 

 

 

 
 responseFormat 

 
 
 
 Field Type 

 GenAiPromptTemplateResponseFormat ( enumeration of type string) 

 
 
 Description 

 Defines the response format. Values are: 
 HTML

 JSON

 MarkDown

 

 

 
 

 

 

 
 status 

 
 
 
 Field Type 

 GenAiPromptTemplateStatus ( enumeration of type string) 

 
 
 Description 

 Required. Indicates the status of the prompt template in Prompt Builder.
 Valid values are: 
 
 Published —Published version of a
 prompt template. The active version of the prompt template must be
 published. Published prompt templates can't be edited with UI or
 Metadata API.

 
 Draft —Draft version of a prompt
 template.

 

 

 
 

 

 

 
 templateDataProviders 

 
 
 
 Field Type 

 
 GenAiPromptTemplateDataProvider [] 

 
 
 Description 

 An array of prompt template data providers associated with the prompt
 template version. 

 
 

 

 

 
 versionNumber 

 
 
 
 Field Type 

 int 

 
 
 Description 

 Required. Version number of the prompt template version. Versions are
 counted sequentially from 1. This tag will be deprecated in 63.0
 and will not work in 64.0 and later. Use versionIdentifier instead.

 

 
 

 

 

 
 versionIdentifier 

 
 
 
 Field Type 

 string 

 
 
 Description 

 
 Version identifier of the prompt template version identifier.
 This is generated automatically once a template is deployed and retrieved
 from an org. 

 If a unique value is not specified then it will be generated for you. It
 must be unique for each version for a given template.

 

 
 

 

 

 

 

 

 
 GenAiPromptTemplateGenerationConfig

 
 References the policies for this prompt template version. A policy describes high-level
 behavior for the prompt template, such as the allowed languages, conversation style, or
 desired response length. Currently, a policy is defined in a configuration file.

 
 
 
 
 
 
 Field Name 

 Description 

 

 

 
 
 generationConfigDeveloperName 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Developer name of the policy for this prompt template version. 

 
 

 

 

 

 

 

 
 GenAiPromptTemplateInput

 
 Represents an input for a prompt template, such as a Salesforce record, field, or Apex
 primitive data type.

 
 
 
 
 
 
 Field Name 

 Description 

 

 

 
 
 apiName 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Required. Name of the prompt template input parameter. 

 
 

 

 
 

 
 definition 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Required. The URI definition of the input parameter. For example, SOBJECT://Account and SOBJECT://Account/Description . 

 
 

 

 
 

 
 description 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Description of the prompt template input parameter. 

 
 

 

 
 

 
 masterLabel 

 
 
 
 Field Type 

 string 

 
 
 Description 

 A user-friendly name for GenAiPromptTemplateInput, which is defined when the
 GenAiPromptTemplateInput is created. 

 
 

 

 
 

 
 referenceName 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Required. Name of the prompt template input to use in expressions. For
 example, Input:Recipient and Input:Sender</referenceName> . 

 
 

 

 

 
 required 

 
 
 
 Field Type 

 boolean 

 
 
 Description 

 Required. Specifies whether this input parameter is required ( true ) or optional ( false ). 

 
 

 

 

 

 

 

 
 GenAiPromptTemplateDataProvider

 
 Represents a source of data for a prompt template version, such as an invocable action,
 flow, or Apex method.

 
 
 
 
 
 
 Field Name 

 Description 

 

 

 
 
 definition 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Required. The URI definition of the data provider, such as flow://ns__CallToActionFlow . 

 
 

 

 
 

 
 description 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Description of the data provider. 

 
 

 

 

 
 label 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Required. A user-friendly name for GenAiPromptTemplateDataProvider, which is
 defined when the GenAiPromptTemplateDataProvider is created. 

 
 

 

 

 
 parameters 

 
 
 
 Field Type 

 
 GenAiPromptTemplateDataProviderParam [] 

 
 
 Description 

 An array of parameters associated with the data provider. 

 
 

 

 
 

 
 referenceName 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Required. Name of the data provider to use in expressions. 

 
 

 

 
 

 

 

 

 
 GenAiPromptTemplateDataProviderParam

 
 Represents a parameter that a data provider uses to retrieve information.

 
 
 
 
 
 
 Field Name 

 Description 

 

 

 
 
 definition 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Required. URI definition of the parameter. For example, SOBJECT://User</definition> . 

 
 

 

 
 

 
 isRequired 

 
 
 
 Field Type 

 boolean 

 
 
 Description 

 Required. Specifies whether the parameter is required ( true ) or optional ( false ). 

 
 

 

 
 

 
 parameterName 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Required. Name of the parameter. 

 
 

 

 
 

 
 valueExpression 

 
 
 
 Field Type 

 string 

 
 
 Description 

 Value or expression of the parameter to use in prompt template text. For
 example, {!$Input:Recipient} . 

 
 

 

 
 

 

 

 

 
 Declarative Metadata Sample Definition

 
 The following is an example of a GenAiPromptTemplate component.

 <?xml version= "1.0" encoding= "UTF-8"?>
 <GenAiPromptTemplate xmlns= "http://soap.sforce.com/2006/04/metadata">
 <activeVersionIdentifier>a94ACO8feseESrBtllQUNLvKEqlCHiPSDLX5rXUnvPs= _1 </activeVersionIdentifier >
 <description >Recommend relevant financial products to client based on their needs and goals </description >
 <masterLabel >Recommend Relevant Products </masterLabel >
 <relatedEntity >Contact </relatedEntity >
 <templateVersions >
 <content >You are a financial advisor at {!$Input:Sender.CompanyName} and your name is {!$Input:Sender.Name}. You are writing an email to a prospective client recommending relevant financial products based on their data and goals. Reference the data below to generate your email, recommending only relevant products for the customer that match our recommendation criteria for each product.
Client name: {!$Input:Recipient.Name}
Client age: {!$Input:Recipient.Age__c}
Client occupation: {!$Input:Recipient.Occupation__c}
Client income: {!$Input:Recipient.Income__c}
Client financial goals: {!$Input:Recipient.Financial_Goals__c}

{!$Flow:Fetch_Products.Prompt}

Generate a subject line that can increase the open rate using words and content that is related to the email body content. It must be no more than 10 words.
Start the opening message of the email with an ice-breaker talking about relevant challenges or opportunities with personal finance and how you can help.
Indirectly allude to a point of common interest, shared background, or relevant experience with {!$Input:Recipient.Name}. You aim to subtly reference or highlight this connection to establish rapport, demonstrate relevance, and foster a sense of familiarity.
Indirectly encourage the lead {!$Input:Recipient.Name} to respond to your email by showing that you are willing to discuss opportunities for working together and answer any questions they may have.
Be concise in your email. </content >
 <inputs >
 <apiName >Sender </apiName >
 <definition >SOBJECT://User </definition >
 <referenceName >Input:Sender </referenceName >
 <required >true </required >
 </inputs >
 <inputs >
 <apiName >Recipient </apiName >
 <definition >SOBJECT://Contact </definition >
 <referenceName >Input:Recipient </referenceName >
 <required >true </required >
 </inputs >
 <primaryModel >sfdc_ai__DefaultOpenAIGPT4 </primaryModel >
 <status >Published </status >
 <templateDataProviders >
 <definition >flow://Fetch_Products </definition >
 <parameters >
 <definition >SOBJECT://User </definition >
 <isRequired >true </isRequired >
 <parameterName >Sender </parameterName >
 <valueExpression >{!$Input:Sender} </valueExpression >
 </parameters >
 <parameters >
 <definition >SOBJECT://Contact </definition >
 <isRequired >true </isRequired >
 <parameterName >Recipient </parameterName >
 <valueExpression >{!$Input:Recipient} </valueExpression >
 </parameters >
 <referenceName >Flow:Fetch_Products </referenceName >
 </templateDataProviders >
 <versionIdentifier>a94ACO8feseESrBtllQUNLvKEqlCHiPSDLX5rXUnvPs= _1
 </versionIdentifier >
 </templateVersions >
 <type >einstein_gpt__salesEmail </type >
 <visibility >Global </visibility >
 </GenAiPromptTemplate >

 The following is an example package.xml that
 references the previous definition.

 <?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
 <types>
 <members>*</members>
 <name>GenAiPromptTemplate</name>
 </types>
 <version>60.0</version>
</Package>

 

 
 Wildcard Support in the Manifest File

 
 This metadata type supports the wildcard character * (asterisk) in the package.xml manifest
 file. For information about using the manifest file, see Deploying and Retrieving Metadata with the Zip
 File .
