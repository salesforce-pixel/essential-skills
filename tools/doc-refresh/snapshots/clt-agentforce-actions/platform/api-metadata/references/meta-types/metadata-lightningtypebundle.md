# LightningTypeBundle

Represents a custom Lightning type. Use this type to override the default user interface to create a customized appearance based on your business requirements. Deploy this bundle to your organization to implement the overrides.

:::important
Where possible, we changed noninclusive terms to align with our company value of Equality. We maintained certain terms to avoid any effect on customer implementations.
:::

## Parent Type

This type extends [Metadata](/docs/platform/api-metadata/references/meta-types/metadata-metadata.md) and inherits its fields.

## File Suffix and Directory Location

LightningTypeBundle components are stored in the `lightningTypes` folder.

Here’s an example of the `LightningTypeBundle` structure.

```
+--myMetadataPackage
    +--lightningTypes (1)
        +--TYPE_NAME (2)
           +--schema.json (3)
           +--CHANNEL_NAME (4)
              +--editor.json (5) OR +--renderer.json (6)
```

The bundle includes these resources.

- The `lightningTypes` folder (1) contains a folder for each created custom Lightning type in the format `{typeName}` (2).
- Each custom lightning type folder contains a `schema.json` file (3) that defines the JSON schema that drives the custom Lightning type validation.
- Optional channel-specific folders (4). To override the default UI for a specific Salesforce application, the bundle contains a folder named after that channel. The supported channel folders are:
  - `lightningDesktopGenAi` (Agentforce Employee agent in Lightning Experience)
  - `enhancedWebChat` (Agentforce Service agent via Enhanced Chat v2)
  - `lightningMobileGenAi` (Agentforce Employee agent on Mobile and Agentforce Service agent via Enhanced Chat v2 on Mobile)
  - `experienceBuilder` (Experience Builder)
  Inside the `{channelName}` folder, you can configure:
  - The `editor.json` file (5) containing custom user interface and editor information
  - The `renderer.json` file (6) containing custom user interface and renderer information
    > **Note:** This file isn’t supported in `experienceBuilder`.

## Version

Introduced in API version 64.0.

## Fields

### description

- **Type:** string
- **Required:** No
- **Description:** Describes the lightning type.

### masterLabel

- **Type:** string
- **Required:** Yes
- **Description:** Required. Represents the name of a LightningTypeBundle which is defined when the LightningTypeBundle is created.

### resources

- **Type:** [LightningTypeBundleResource\[\]](#lightningtypebundleresource-type)
- **Required:** No
- **Description:** The list of resource files in the `lightningTypes` folder.

## LightningTypeBundleResource Type

Represents a resource inside a LightningTypeBundle.

### Fields

#### fileName

- **Type:** string
- **Required:** Yes
- **Description:** Required. Name of the resource file.

#### filePath

- **Type:** string
- **Required:** Yes
- **Description:** Required. Path of the resource file.

#### fileType

- **Type:** string
- **Required:** Yes

#### source

- **Type:** base64Binary
- **Required:** Yes
- **Description:** Required. The JSON content of the resource.

## Declarative Metadata Sample Definition

This `package.xml` file retrieves all the LightningTypeBundle components in an org.

```
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>*</members>
        <name>LightningTypeBundle</name>
    </types>
    <version>64.0</version>
</Package>
```

In the retrieved `.zip` file, each custom Lightning type is nested under a `lightningTypes` folder.

This example shows the directory structure in the `.zip` file of a custom Lightning type named `flightResponse`:

```
+--lightningTypes
    +--flightResponse
        +--schema.json
        +--lightningDesktopGenAi
            +--renderer.json
```

In this example, the custom Lightning type `flightResponse` is a complex type that references an Apex class named `Flight`.

```
global class Flight {

    @AuraEnabled
    global String flightId;

    @AuraEnabled
    global Integer numLayovers;

    @AuraEnabled
    global Boolean isPetAllowed;

    @AuraEnabled
    global Long price;

    @AuraEnabled
    global Double discountPercentage;

    @AuraEnabled
    global Integer durationInMin;

    global Flight(String flightId, Integer numLayovers, Boolean isPetAllowed,
                  Long price, Double discountPercentage, Integer durationInMin) {
        this.flightId = flightId;
        this.numLayovers = numLayovers;
        this.isPetAllowed = isPetAllowed;
        this.price = price;
        this.discountPercentage = discountPercentage;
        this.durationInMin = durationInMin;
     }
}
global class FlightRequestFilter {

    @AuraEnabled
    global Long price;

    @AuraEnabled
    global Double discountPercentage;
}
```

Here are the contents of the files in the `flightResponse` directory. This sample code shows the contents of the `schema.json` file.

```
{
  "title": "My Flight Response",
  "description": "My Flight Response",
  "lightning:type": "@apexClassType/c__Flight"
}
```

The `lightningDesktopGenAi` folder (optional) includes a `renderer.json` file that overrides the default UI of the custom Lightning type `flightResponse` when you use the `Flight` Apex class as an output parameter for an agent action.

Contents of the `renderer.json` file.

```
{
  "renderer": {
    "componentOverrides": {
      "$": {
        "definition": "c/flightDetails"
      }
    }
  }
}
```

:::note
flightDetails is a custom LWC component referenced in `renderer.json` file.
:::

This example shows the directory structure in the `.zip` file of a custom Lightning type named `flightFilter`:

```
+--lightningTypes
    +--flightFilter
        +--schema.json
        +--lightningDesktopGenAi
            +--editor.json
```

In this example, the custom Lightning type `flightFilter` is a complex type that references an Apex class named `FlightRequestFilter`.

```
global class Flight {

    @AuraEnabled
    global String flightId;

    @AuraEnabled
    global Integer numLayovers;

    @AuraEnabled
    global Boolean isPetAllowed;

    @AuraEnabled
    global Long price;

    @AuraEnabled
    global Double discountPercentage;

    @AuraEnabled
    global Integer durationInMin;

    global Flight(String flightId, Integer numLayovers, Boolean isPetAllowed,
                  Long price, Double discountPercentage, Integer durationInMin) {
        this.flightId = flightId;
        this.numLayovers = numLayovers;
        this.isPetAllowed = isPetAllowed;
        this.price = price;
        this.discountPercentage = discountPercentage;
        this.durationInMin = durationInMin;
     }
}
global class FlightRequestFilter {

    @AuraEnabled
    global Long price;

    @AuraEnabled
    global Double discountPercentage;
}
```

Here are the contents of the files in the `flightFilter` directory. This sample code shows the contents of the `schema.json` file.

```
{
  "title": "Flight Filter",
  "description": "Flight Filter",
  "lightning:type": "@apexClassType/c__FlightRequestFilter"
}
```

The `lightningDesktopGenAi` folder (optional) includes an `editor.json` file that overrides the default UI of the custom Lightning type `flightFilter` when you use the `Flight` Apex class as an input parameter for an agent action.

Contents of the `editor.json` file.

```
{
  "editor": {
    "componentOverrides": {
      "$": {
        "definition": "c/flightFilter"
      }
    }
  }
}
```

:::note
flightFilter is a custom LWC component referenced in `editor.json` file.
:::

## Wildcard Support in the Manifest File

This metadata type supports the wildcard character `*` (asterisk) in the `package.xml` manifest file. For information about using the manifest file, see [Deploying and Retrieving Metadata with the Zip File](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/file_based_zip_file.htm).
