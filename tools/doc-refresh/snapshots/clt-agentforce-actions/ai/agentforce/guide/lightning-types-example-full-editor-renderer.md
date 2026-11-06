# Example: Customizing User Interface Using Custom Lightning Types with Top-Level Editor and Top-Level Renderer Overrides

This example explains how to override the default user interface to create a customized appearance of responses on the custom agent’s action input and output with custom Lightning types.

In this example, you specify an editor override and a renderer override for the custom Lightning type that you created.

## Before You Begin

Download these sample data files.

- [apexClass.zip](https://resources.docs.salesforce.com/rel1/doc/en-us/static/misc/apexClassExample.zip)
- [flightResponseCLTandLWC.zip](https://resources.docs.salesforce.com/rel1/doc/en-us/static/misc/flightResponseCLTAndLWC4.zip)
- [flightFiltersCLTandLWC.zip](https://resources.docs.salesforce.com/rel1/doc/en-us/static/misc/flightFilterCLTAndLWCExample.zip)

## Example Apex Class for Retrieving Flight Information

Use these Apex classes together to create a custom agent action that finds flights. The main `FlightAgent` class contains the invocable method, and the other classes define the complex data structures for the request and response.

When you create your custom agent action, select the method **Find Flights**.

**FlightAgent Class**

This class is the main class that contains the logic for the `Find Flights` agent action. It also defines the `FlightRequest` and `FlightResponse` inner classes to handle the action's input and output.

```apex
global class FlightAgent {

    @InvocableMethod(label='Find Flights' description='Finds available flights')
    global static List<FlightResponse> findFlights(List<FlightRequest> req) {
        List<FlightResponse> flightResponses = new List<FlightResponse>();

        // For example, we hardcode the data and don’t focus on how we retrieve it.
        // However, consider that we receive available flight data from a service
        // and then iterate through the data to generate the final response.

        List<Flight> flights = new List<Flight>();
        Flight f1 = new Flight('IX 2814', 1, false, 1000l, 20.20d, 70);
        Flight f2 = new Flight('6E 488', 2, false, 2000l, 15.15d, 120);
        Flight f3 = new Flight('6E 523', 1, false, 3000l, 13.14d, 75);
        Flight f4 = new Flight('6E 6166', 2, false, 4000l, 14.14d, 130);
        flights.add(f1);  flights.add(f2); flights.add(f3); flights.add(f4);
        AvailableFlight availableFlights = new AvailableFlight();
        availableFlights.flights = flights;

        FlightResponse fr = new FlightResponse();
        fr.aFlight = availableFlights;
        flightResponses.add(fr);

        return flightResponses;
    }

    @JsonAccess(serializable='always' deserializable='always')
    global class FlightRequest {

        @InvocableVariable
        global String originCity;

        @InvocableVariable
        global String destinationCity;

        @InvocableVariable
        global Date dateOfTravel;

        @InvocableVariable
        global FlightRequestFilter filters;
    }

    @JsonAccess(serializable='always' deserializable='always')
    global class FlightResponse {

        @InvocableVariable
        global AvailableFlight aFlight;
    }
}
```

**AvailableFlight Class**

This class defines a list that holds multiple Flight objects.

```apex
@JsonAccess(serializable='always' deserializable='always')
global class AvailableFlight {

    @AuraEnabled
    global List<Flight> flights;
}
```

**Flight Class**

This class defines the data structure for flight details.

```apex
@JsonAccess(serializable='always' deserializable='always')
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
```

**FlightRequestFilter**

This class defines the data structure for the optional filters a user can apply when searching for flights.

```apex
@JsonAccess(serializable='always' deserializable='always')
global class FlightRequestFilter {

    @AuraEnabled
    global Long price;

    @AuraEnabled
    global Double discountPercentage;
}
```

The Apex class `FlightAgent` accepts the flight search criteria, including the origin city, destination city, and date of travel, and then returns a list of available flights.

:::note
For this example, flight availability data is already included in the `FlightAgent` Apex class. However, in a real-time scenario, flight information is fetched from an external service, and the Apex class processes that data to generate the final response.
:::

## Set Up the Agent and Action in Agentforce Builder

Before you can add custom Lightning types to agent actions, create the agent and configure it to use your Apex class.

1. From the **Agentforce Studio** app, create a new Agentforce Employee Agent or Agentforce Service Agent and name it (for example, `Flight Search Agent`).
2. Open your agent, create a new subagent named `Flight Search`, and open it to add actions.
3. Add a new action named `Find Flights` to your subagent, set the `Reference Action Type` to **Apex**, and select the **Find Flights** method from the `FlightAgent` class you deployed earlier.
4. Switch to Script mode and add `is_user_input: True` to each input that the agent collects from the user.
5. In the Flight Search subagent, add instructions that tell the agent when to use the action and what data to collect. For example: "When a customer asks about flight availability or wants to search for flights, use the {!@actions.Find_Flights} action. Collect the origin city, destination city, and date of travel from the customer before running the action."

This code shows the `Flight_Search` subagent and `Find_Flights` action that the preceding steps create. To create the same configuration directly, add this code to the agent script.

```agentscript
subagent Flight_Search:
    label: "Flight Search"
    description: |

        Search flights
    reasoning:
        instructions: ->
            | When a customer asks about flight availability or wants to search for flights, use the {!@actions.Find_Flights} action. Collect the origin city, destination city, and date of travel from the customer before running the action.
        actions:
            Find_Flights: @actions.Find_Flights
                with dateOfTravel = ...
                with destinationCity = ...
                with filters = ...
                with originCity = ...


    actions:
        Find_Flights:
            label: "Find Flights"
            description: "find available flights"
            target: "apex://FlightAgent"
            inputs:
                dateOfTravel: object
                    label: "dateOfTravel"
                    is_required: True
                    is_user_input: True
                    complex_data_type_name: "lightning__dateType"
                    description: "date info"
                destinationCity: string
                    label: "destinationCity"
                    is_required: True
                    is_user_input: True
                    description: "city info"
                filters: object
                    label: "filters"
                    is_required: True
                    is_user_input: True
                    complex_data_type_name: "@apexClassType/c__FlightRequestFilter"
                    description: "filters"
                originCity: string
                    label: "originCity"
                    is_required: True
                    is_user_input: True
                    description: "city"
            outputs:
                aFlight: object
                    label: "aFlight"
                    complex_data_type_name: "@apexClassType/c__AvailableFlight"
                    is_displayable: True
                    filter_from_agent: False
                    description: "result"
```

When you add the code directly to the agent script, also add this transition to the Agent Router’s `actions` section to route flight-search requests to the `Flight Search` subagent.

```agentscript
go_to_Flight_Search: @utils.transition to @subagent.Flight_Search
```

This image shows the transition in the Agent Router’s actions section.

![Agent Router in Script mode with the go_to_Flight_Search transition in its actions section.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/flight-agent.png)

:::note
Agent Script identifiers are case-sensitive. The `@subagent.Flight_Search` reference must match the identifier in the subagent `Flight_Search` declaration.
:::

**See Also**

- [Create an Agent](https://help.salesforce.com/s/articleView?id=ai.agent_setup_create.htm\&type=5)
- [Create a Custom Subagent](https://help.salesforce.com/s/articleView?id=ai.agent_topics_add_custom.htm\&type=5)
- [Create a Custom Action](https://help.salesforce.com/s/articleView?id=ai.agent_actions_custom.htm\&type=5)
- [Add an Action to a Subagent from the Asset Library](https://help.salesforce.com/s/articleView?id=ai.agent_actions_add_asset_library.htm\&type=5)
- [How Subagent Instructions are Resolved to Build a Prompt](https://help.salesforce.com/s/articleView?id=ai.agent_topics_instructions_resolve.htm\&type=5)

## Action Inputs and Outputs

Inputs and outputs for the agent action are defined by using standard Lightning types and Apex classes.

Input:

- `dateOfTravel`, `destinationCity`, and `originCity` use standard Lightning types such as lightning\_\_dateType and lightning\_\_textType.
- The `filters` input is a complex type that references an Apex class.

Output:

- The output `aFlight` for the agent action is a complex type that references an Apex class.

Here’s an image that shows the custom agent action created.

![Input and output settings for a 'Find Flights' agent action. Inputs: dateOfTravel, destinationCity, filters, originCity. Output: aFlight.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/flight-update.png)

The available flight information is retrieved by using `@apexClassType/c__AvailableFlight` in the agent action output, where:

- `apexClassType` is the bundle name.
- `AvailableFlight` is the Apex class.

When you execute this agent action, it prompts you to provide input and then generates the output.

## Agent Action Execution Input

The agent’s action UI collects these details to find available flights.

- Origin city
- Destination city
- Date of travel

Here’s the image that shows how the custom agent action input appears in an agent conversation.

![Agent's response to collect flight details. The response lacks filter details for price and discount percentage, making it difficult to filter flight data.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/Example1-Input-Action.png)

## Agent Action Execution Output

The agent’s action UI returns the available flight details.

Here’s the image that shows how the custom agent action’s output appears in an agent conversation.

![Agent's response to a flight details request. The response lacks labels and is presented in a format that is hard to understand.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/Example-Execution-Output.png)

## Result Data

The agent displays the flight data in the response.

Here’s the sample code that shows the available flight data.

```json
{
  "aFlight": {
    "flights": [
      {
        "price": 1000,
        "numLayovers": 1,
        "isPetAllowed": false,
        "flightId": "IX 2814",
        "durationInMin": 70,
        "discountPercentage": 20.2,
        "departureTime": "08:30"
      },
      {
        "price": 2000,
        "numLayovers": 2,
        "isPetAllowed": true,
        "flightId": "6E 488",
        "durationInMin": 120,
        "discountPercentage": 15.15,
        "departureTime": "09.00"
      }
    ]
  }
}
```

## Customize UI for Output

Create a custom Lightning type named `flightResponse` to enhance the visibility of the information in the output UI.

### Override Default UI for Output With Custom Lightning Types

Override the agent’s action UI for output to enhance the user experience by using Custom Lightning Types (CLTs). With CLTs, you can add your own Lightning Web Components (LWC) to present data in a more structured and intuitive format.

Configure the `renderer.json` file to override the default UI of a custom Lightning type in the agent action.

Here’s an example showing a lightningTypes folder for a custom Lightning type named `flightResponse`.

```
+--lightningTypes
        +--flightResponse
            +--schema.json
            +--lightningDesktopGenAi
               +--renderer.json

```

:::note
This example uses `lightningDesktopGenAi` to configure the custom Lightning type. To configure the type for the `enhancedWebChat` channel, create the `renderer.json` file in the corresponding channel folder.
:::

This image shows an example of the `flightResponse` folder structure.

![The flightResponse folder contains schema.json and the enhancedWebChat and lightningDesktopGenAi folders. Each channel folder contains a renderer.json file.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/output-folder.png)

The custom Lightning type `flightResponse` includes a `schema.json` file and a `renderer.json` file. The `renderer.json` file controls how the data is displayed to the user in the agent action output.

This sample code shows the contents of the `schema.json` file.

```json
{
  "title": "My Flight Response",
  "description": "My Flight Response",
  "lightning:type": "@apexClassType/c__AvailableFlight"
}
```

This sample code shows the contents of the `renderer.json` file.

```json
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

**See Also**

- *Metadata API Developer Guide*: [LightningTypeBundle](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_lightningtypebundle.htm)

### Build Output Components with Lightning Web Components

This section explains how the components are created and deployed for agent action output.

This image shows the Lightning Web Component (LWC) folder structure.

![The lwc folder contains a folder named flightDetails, which is the LWC component. The flightDetails folder includes CSS, HTML, JS, and metadata files.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/Example1-Output-LWC.png)

The LWC component includes HTML markup designed to represent the data that the agent returns for `@apexClassType/c__AvailableFlight`. This HTML markup ensures that the data is displayed in an intuitive and customized format.

This sample code shows the contents of the `flightDetails.js-meta.xml` file.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>64.0</apiVersion>
    <isExposed>true</isExposed>
    <masterLabel>Flight LWC</masterLabel>
    <targets>
      <target>lightning__AgentforceOutput</target>
    </targets>
    <targetConfigs>
      <targetConfig targets="lightning__AgentforceOutput">
        <sourceType name="c__flightResponse"/>
      </targetConfig>
    </targetConfigs>
</LightningComponentBundle>
```

:::note
When you create an LWC component to override the UI for action input, use `lightning__AgentforceInput` as the target. For output, use `lightning__AgentforceOutput`. For information about LWC target types, see [`lightning__AgentforceInput` Target](https://developer.salesforce.com/docs/platform/lwc/guide/targets-lightning-agentforce-input.md) and [`lightning__AgentforceOutput`Target](https://developer.salesforce.com/docs/platform/lwc/guide/targets-lightning-agentforce-output.md).
:::

This sample code shows the contents of the `flightDetails.html` file.

```html
<template>
    <lightning-card icon-name="standard:flight" class="flight-card-container">
    <span class="flightTitle">AvailableFlights</span>
        <!-- Flight Cards List -->
        <div class="flight-list-container">
            <template for:each={flightData} for:item="flight">
                <div key={flight.flightId} class="flight-card">
                    <!-- Flight Info Section -->
                    <div class="flight-info">
                        <h2 class="flight-id">{flight.flightId}</h2>
                        <div class="discount-tag">{flight.discountPercentage}% Off</div>
                    </div>

                    <!-- Flight Price, Duration, Departure and Arrival -->
                    <div class="price-duration">
                        <div class="price">
                            <strong>${flight.price}</strong>
                        </div>
                        <div class="duration">
                            {flight.durationInHr}
                        </div>
                    </div>

                    <!-- Timeline for Departure, Duration and Arrival -->
                    <div class="flight-timeline">
                        <div class="timeline">
                            <div class="time-point departure">
                                <span>Departure Time: {flight.departureTime}</span>
                            </div>
                            <div class="time-point arrival">
                                <span>Arrival Time: {flight.arrivalInHr}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Additional Info Section (Layovers, Pets, etc.) -->
                    <div class="additional-info">
                        <div class="layovers">
                            <lightning-icon icon-name="utility:loop" size="small"></lightning-icon>
                            <span>Layovers: {flight.numLayovers}</span>
                        </div>
                        <div class="pets">
                            <lightning-icon icon-name="utility:paw" size="small"></lightning-icon>
                            <span>Pets Allowed: {flight.petAllowedStatus}</span>
                        </div>
                    </div>
                    
                </div>
            </template>
        </div>
    </lightning-card>
</template>
```

This sample code shows the contents of the `flightDetails.js` file.

```javascript
import { LightningElement, api } from "lwc";

export default class FlightDetails extends LightningElement {
  @api value;
  flightData = [];

  // Method to convert duration from minutes to hours and minutes
  formattedDuration(durationInMin) {
    if (durationInMin) {
      const hours = Math.floor(durationInMin / 60); // Get whole hours
      const minutes = durationInMin % 60; // Get remaining minutes
      return `${hours} hr ${minutes} min`;
    }
    return;
  }

  // Method to calculate arrival time based on departure time and duration
  arrivalTime(durationInMin) {
    const hours = 7,
      minutes = 0;
    const departureDate = new Date(2025, 0, 1, hours, minutes); // Sample date for calculation

    const arrivalDate = new Date(departureDate.getTime() + durationInMin * 60000); // Add duration to departure time

    const arrivalHours = String(arrivalDate.getHours()).padStart(2, "0");
    const arrivalMinutes = String(arrivalDate.getMinutes()).padStart(2, "0");

    return `${arrivalHours}:${arrivalMinutes}`;
  }

  connectedCallback() {
    const flights = this.value?.flights || [];
    this.flightData = flights.map((flight) => ({
      ...flight,
      petAllowedStatus: flight.isPetAllowed ? "Yes" : "No",
      durationInHr: this.formattedDuration(flight.durationInMin),
      departureTime: "07:00",
      arrivalInHr: this.arrivalTime(flight.durationInMin),
    }));
  }
}
```

**See Also**

- *Lightning Web Components Developer Guide*: [Get Started with Lightning Web Components](https://developer.salesforce.com/docs/platform/lwc/guide)

### Configure Custom Lightning Type for Output in Agent Script

After you create a custom Lightning type and Lightning Web Component, configure the agent action to use them.

1. In **Agentforce Builder**, open your agent.
2. In the **Explorer** panel, go to your subagent and select the **Find Flights** action.
3. Switch to **Script** mode using the toggle at the top of the canvas.
4. Locate the `aFlight` output parameter in the action configuration
5. Replace the existing value of the `complex_data_type_name` property ‌with `c__flightResponse`. Custom Lightning types use the `c__` namespace prefix.
6. Click **Save**.

:::note
The script will fail validation if you specify a non-existent custom Lightning type name.
:::

Here's an image that shows the custom Lightning type configured in Script mode:

![The agent action outputs parameter with 'c\_\_flightResponse' selected in the complex_data_type_name property.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/flight-output.png)

**See Also**

- [Agent Script Reference: Actions](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-ref-actions.md#outputs)

## Customize UI for Input

Create a custom Lightning type named `flightFilter` to show filters in the input UI that suits your business needs.

### Override Default UI for Input with Custom Lightning Types

Override the agent’s action UI for input to enhance the user experience by using Custom Lightning Types (CLTs). With CLTs, you can add your own Lightning Web Components (LWC) to present data in a more structured and intuitive format

Configure the `editor.json` file to override the default UI of a custom Lightning type in the agent action.

Here’s an example that shows a lightningTypes folder for a custom Lightning type named `flightFilter`.

```
+--lightningTypes
        +--flightFilter
            +--schema.json
            +--lightningDesktopGenAi
               +--editor.json
```

:::note
This example uses `lightningDesktopGenAi` to configure the custom Lightning type. To configure the type for the `enhancedWebChat` channel, create the `editor.json` file in the corresponding channel folder.
:::

This image shows an example of the `flightFilter` folder structure.

![The flightFilter folder contains schema.json and the enhancedWebChat and lightningDesktopGenAi folders. Each channel folder contains an editor.json file.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/input-folder.png)

The custom Lightning type `flightFilter` includes a `schema.json` file and an `editor.json` file. The `editor.json` file controls how the data is displayed to the user in the agent action input.

This sample code shows the contents of the `schema.json` file.

```json
{
  "title": "Flight Filter",
  "description": "Flight Filter",
  "lightning:type": "@apexClassType/c__FlightRequestFilter"
}
```

This sample code shows the contents of the `editor.json` file.

```json
{
  "editor": {
    "componentOverrides": {
      "$": {
        "definition": "c/flightRequestFilter"
      }
    }
  }
}
```

**See Also**

- *Metadata API Developer Guide*: [LightningTypeBundle](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_lightningtypebundle.htm)

### Build Input Components with Lightning Web Components

This section explains how the components are created and deployed for agent action input.

This image shows the Lightning Web Component (LWC) folder structure.

![The lwc folder contains a folder named flightRequestFilter, which is the LWC component. The flightRequestFilter folder includes CSS, HTML, JS, and metadata files.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/Example1-Input-LWC.png)

The LWC component includes HTML markup designed to accept input for `@apexClassType/c__FlightRequestFilter`. This HTML markup ensures that the data is displayed in an intuitive and customized format.

This sample code shows the contents of the `flightRequestFilter.js-meta.xml` file.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>64.0</apiVersion>
    <isExposed>true</isExposed>
    <masterLabel>Flight Filter LWC</masterLabel>
    <targets>
      <target>lightning__AgentforceInput</target>
    </targets>
    <targetConfigs>
      <targetConfig targets="lightning__AgentforceInput">
        <targetType name="c__flightFilter"/>
      </targetConfig>
    </targetConfigs>
</LightningComponentBundle>
```

:::note
When you create an LWC component to override the UI for action input, use `lightning__AgentforceInput` as the target. For output, use `lightning__AgentforceOutput`. For information about LWC target types, see [`lightning__AgentforceInput` Target](https://developer.salesforce.com/docs/platform/lwc/guide/targets-lightning-agentforce-input.md) and [`lightning__AgentforceOutput` Target](https://developer.salesforce.com/docs/platform/lwc/guide/targets-lightning-agentforce-output.md).
:::

This sample code shows the contents of the `flightRequestFilter.html` file.

```html
<template>
    <lightning-card title="Price and Discount Percentage">
        <div class="slds-p-horizontal_medium">
            <!-- Price input -->
            <lightning-input 
                label="Enter Price (between 1,000 and 20,000)" 
                name="price"
                value={price} 
                type="number" 
                min="1000" 
                max="20000" 
                step="1"
                onchange={handleInputChange}
                read-only={readOnly}>
            </lightning-input>

            <!-- Discount Percentage input -->
            <lightning-input 
                label="Enter Discount Percentage (0% to 100%)" 
                name="discountPercentage"
                value={discountPercentage} 
                type="number" 
                min="0" 
                max="100" 
                step="1"
                onchange={handleInputChange}
                read-only={readOnly}>
            </lightning-input>
        </div>
    </lightning-card>
</template>
```

This sample code shows the contents of the `flightRequestFilter.js` file.

```javascript
import { api, LightningElement } from "lwc";
export default class FlightFilter extends LightningElement {
  @api
  get readOnly() {
    return this._readOnly;
  }

  set readOnly(value) {
    this._readOnly = value;
  }
  _readOnly = false;
  _value;
  @api
  get value() {
    return this._value;
  }
  set value(value) {
    this._value = value;
  }
  price;
  discountPercentage;

  connectedCallback() {
    if (this.value) {
      this.price = this.value?.price || "";
      this.discountPercentage = this.value?.discountPercentage || "";
    }
  }
  handleInputChange(event) {
    event.stopPropagation();
    const { name, value } = event.target;
    this[name] = value;
    this.dispatchEvent(
      new CustomEvent("valuechange", {
        detail: {
          value: {
            price: this.price,
            discountPercentage: this.discountPercentage,
          },
        },
      }),
    );
  }
}
```

:::note
You must include the `handleInputChange()` function to capture user input, update the component’s state, and notify the parent component (planner component) by using the valuechange event. The function ensures real-time data binding and prevents unwanted event propagation.
:::

**See Also**

- *Lightning Web Components Developer Guide*: [Get Started with Lightning Web Components](https://developer.salesforce.com/docs/platform/lwc/guide)

### Configure Custom Lightning Type for Input in Agent Script

After you create a custom Lightning type and Lightning Web Component, configure the agent action to use them.

1. In **Agentforce Builder**, open your agent.
2. In the **Explorer** panel, go to your subagent and select the **Find Flights** action.
3. Switch to **Script** mode using the toggle at the top of the canvas.
4. Locate the `filters` input parameter in the action configuration.
5. Replace the existing value of the `complex_data_type_name` property with `c__flightFilter`. Custom Lightning types use the `c__` namespace prefix.
6. Click **Save**.

:::note
The script will fail validation if you specify a non-existent custom Lightning type name.
:::

Here's an image that shows the custom Lightning type configured in Script mode:

![The agent action inputs parameter with 'c\_\_flightFilter' selected in the complex_data_type_name property.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/flight-input.png)

:::note
In certain instances the large language model (LLM) requests input as text, so make sure to accurately update the subagent instructions for the correct selection of the Override Input component. For example, when you enter a prompt to find flights, the agent executes the Find Flight action. The Find Flight action executes by taking input through a UI form, and not in the form of Text because it includes a price and discount range.
:::

**See Also**

- [Agent Script Reference: Actions](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-ref-actions.md#outputs)

## Test, Commit, and Activate Your Agent

After you configure the custom Lightning types for both input and output in the agent script, preview the conversation to verify the user experience. Once you're satisfied with the customized UIs, commit and activate your agent to make it available to users.

1. In **Agentforce Builder**, click the **Preview** tab.

2. Enter a test utterance, such as "Find flights."

3. When the agent prompts for filter details, verify that the custom input form displays the price and discount fields exactly as you designed them in `flightFilter`.

   This image shows how the custom agent action’s input appears in an agent conversation.

   ![Agent's response to collect flight details. The response includes filter fields for price and discount percentage, making it easy to filter flight data.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/Example1-Input-Final.png)

4. Submit the form and review the agent's final response to verify that the flight data renders using your custom `flightResponse` LWC cards.

   This image shows how the custom agent action's output appears in an agent conversation:

   ![Agent's response to a flight details request. The response includes clear labels and is presented in a format that is easy to understand.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/example1-output.png)

5. At the top of the canvas, click **Commit Version** and then click **Commit** to confirm.

   :::note
   To make further changes after this point, you must create a new draft from the committed version.
   :::

6. With the committed version selected, click **Activate** and confirm the activation to make the agent available to users. The currently active version (if any) is automatically deactivated.

**See Also**

- [Explore Agentforce Builder](https://help.salesforce.com/s/articleView?id=ai.agent_builder_tour.htm\&type=5)
- [Commit an Agent Version](https://help.salesforce.com/s/articleView?id=ai.agent_versions_commit.htm\&type=5)
- [Activate or Deactivate Your Agent](https://help.salesforce.com/s/articleView?id=ai.copilot_setup_activate_deactivate.htm\&type=5)
