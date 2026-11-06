# Example: Customizing User Interface Using Custom Lightning Types with Top-Level Collection Renderer Override

This example explains how to override the default user interface to create a customized appearance of responses on the custom agent’s action output with custom Lightning types.

In this example, you specify a renderer collection override for the custom Lighting type that you created.

## Before You Begin

Download these sample data files.

- [apexClass.zip](https://resources.docs.salesforce.com/rel1/doc/en-us/static/misc/apexClassesExample.zip)
- [hotelLWCandCLT.zip](https://resources.docs.salesforce.com/rel1/doc/en-us/static/misc/hotelLWCAndCLT4.zip)

## Example Apex Class for Retrieving Hotel Information

Use these Apex classes together to create a custom agent action that finds available hotels. The main `HotelReservation` class contains the invocable method, and the other classes define the complex data structures for the request and response.

When you create your custom agent action, select the method **Find hotels**.

**HotelReservation Class**

This class is the main class that contains the logic for the `find hotels` agent action.

```apex
@JsonAccess(serializable='always' deserializable='always')
global class HotelReservation {
    @InvocableMethod(label='Find hotels ' description='Find Available Hotels')
    global static List<HotelResponse> findHotels(List<HotelRequest> req) {
        // For example, we hardcode the data and don’t focus on how we retrieve it.
        // However, consider that we receive available hotel data from a service
        // and then iterate through the data to generate the final response.

        List<HotelResponse> hotelResponseList = new List<HotelResponse>();

        Room r1 = new Room('DELUX', 2, 15.15d, 2000l, false);
        List<Room> rooms = new List<Room>();
        rooms.add(r1);

        HotelCategory fourStar = new HotelCategory('four');
        Hotel hotel1 = new Hotel('Sahara Hotels', 'Gacchibowli Hyderabad', rooms, fourStar);
        HotelCategory fiveStar = new HotelCategory('five');
        Hotel hotel2 = new Hotel('Taj Vivanta', 'Kokapet', rooms, fiveStar);
        List<Hotel> hotels = new List<Hotel>();
        hotels.add(hotel1);
        hotels.add(hotel2);

        HotelResponse hotelresponse = new HotelResponse(hotels);
        hotelResponseList.add(hotelresponse);

        return hotelResponseList;
    }
}
```

**HotelResponse Class**

This class defines the data structure for the response that returns a list of available hotels.

```apex
@JsonAccess(serializable='always' deserializable='always')
global class HotelResponse {
    @InvocableVariable
    global List<Hotel> hotels;

    global HotelResponse(List<Hotel> hotels) {
        this.hotels = hotels;
    }
}
```

**Hotel Class**

This class defines the data structure for hotel details.

```apex
@JsonAccess(serializable='always' deserializable='always')
global class Hotel {
    @InvocableVariable
    global String name;

    @InvocableVariable
    global String address;

    @InvocableVariable
    global List<Room> rooms;

    @InvocableVariable
    global HotelCategory hotelCategory;

    global Hotel(String name, String address, List<Room> rooms, HotelCategory hotelCategory) {
        this.name = name;
        this.address = address;
        this.rooms = rooms;
        this.hotelCategory = hotelCategory;
    }
}
```

**Room Class**

This class defines the data structure for rooms within a hotel.

```apex
@JsonAccess(serializable='always' deserializable='always')
global class Room {
    @InvocableVariable
    global String type;

    @InvocableVariable
    global Integer available;

    @InvocableVariable
    global Double discountPercentage;

    @InvocableVariable
    global Long price;

    @InvocableVariable
    global Boolean petAllowed;

    global Room(String type, Integer available, Double discountPercentage, Long price, Boolean petAllowed) {
        this.type = type;
        this.available = available;
        this.discountPercentage = discountPercentage;
        this.price = price;
        this.petAllowed = petAllowed;
    }
}
```

**HotelCategory Class**

This class defines the data structure for a hotel’s star rating.

```apex
@JsonAccess(serializable='always' deserializable='always')
global class HotelCategory {
    @InvocableVariable
    global String star;

    global HotelCategory(String star) {
        this.star = star;
    }
}
```

**HotelRequest Class**

This class defines the data structure for the agent action’s input criteria.

```apex
@JsonAccess(serializable='always' deserializable='always')
global class HotelRequest {
    @InvocableVariable
    global String city;

    @InvocableVariable
    global Date checkInDate;

    @InvocableVariable
    global Date checkOutDate;
}
```

The Apex class `Hotel Reservation` accepts the hotel search criteria, including the check in date, check out date, and city, and then returns a list of available hotels.

:::note
For this example, hotel availability data is already included in the `Hotel Reservation` Apex class. However, in a real-time scenario, hotel information is fetched from an external service, and the Apex class processes that data to generate the final response.
:::

## Set Up the Agent and Action in Agentforce Builder

Before you can add custom Lightning types to agent actions, create the agent and configure it to use your Apex class.

1. From the **Agentforce Studio** app, create a new Agentforce Employee Agent or Agentforce Service Agent and name it (for example, `Hotel Search Agent`).
2. Open your agent, create a new subagent named `Hotel Search`, and open it to add actions.
3. Add a new action named `Find hotels` to your subagent, set the `Reference Action Type` to **Apex**, and select the **Find hotels** method from the `HotelReservation` class you deployed earlier.
4. Switch to Script mode and add `is_user_input: True` to each input that the agent collects from the user.
5. In the Hotel Search subagent, add instructions that tell the agent when to use the action and what data to collect. For example: "When a customer asks about hotel availability or wants to search for hotels, use the {!@actions.Find_hotels} action. Collect the checkin date, checkout date, and city from the customer before running the action."

This code shows the `Hotel_Search` subagent and `Find_hotels` action that the preceding steps create. To create the same configuration directly, add this code to the agent script.

```agentscript
subagent Hotel_Search:
    label: "Hotel Search"
    description: |

        Search hotels
    reasoning:
        instructions: ->
            | When a customer asks about hotel availability or wants to search for hotels, use the {!@actions.Find_hotels} action. Collect the checkin date, checkout date, and city from the customer before running the action.
        actions:
            Find_hotels: @actions.Find_hotels
                with checkInDate = ...
                with checkOutDate = ...
                with city = ...


    actions:
        Find_hotels:
            label: "Find hotels"
            description: "find available hotels"
            target: "apex://HotelReservation"
            inputs:
                checkInDate: object
                    label: "checkInDate"
                    is_required: True
                    is_user_input: True
                    complex_data_type_name: "lightning__dateType"
                    description: "checkin date"
                checkOutDate: object
                    label: "checkOutDate"
                    is_required: True
                    is_user_input: True
                    complex_data_type_name: "lightning__dateType"
                    description: "checkout date"
                city: string
                    label: "city"
                    is_required: True
                    is_user_input: True
                    description: "city"
            outputs:
                hotels: list[object]
                    label: "hotels"
                    complex_data_type_name: "@apexClassType/c__Hotel"
                    is_displayable: True
                    filter_from_agent: False
                    description: "result"

```

When you add the code directly to the agent script, also add this transition to the Agent Router’s `actions` section to route hotel-search requests to the `Hotel Search` subagent.

```agentscript
go_to_Hotel_Search: @utils.transition to @subagent.Hotel_Search
```

This image shows the transition in the Agent Router’s actions section.

![Agent Router in Script mode with the go_to_Hotel_Search transition in its actions section.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/hotel-agent.png)

:::note
Agent Script identifiers are case-sensitive. The `@subagent.Hotel_Search` reference must match the identifier in the subagent `Hotel_Search` declaration.
:::

**See Also**

- [Create an Agent](https://help.salesforce.com/s/articleView?id=ai.agent_setup_create.htm\&type=5)
- [Create a Custom Subagent](https://help.salesforce.com/s/articleView?id=ai.agent_topics_add_custom.htm\&type=5)
- [Create a Custom Action](https://help.salesforce.com/s/articleView?id=ai.agent_actions_custom.htm\&type=5)
- [Add an Action to a Subagent from the Asset Library](https://help.salesforce.com/s/articleView?id=ai.agent_actions_add_asset_library.htm\&type=5)
- [How Subagent Instructions are Resolved to Build a Prompt](https://help.salesforce.com/s/articleView?id=ai.agent_topics_instructions_resolve.htm\&type=5)

## Actions Inputs and Outputs

Inputs and outputs for the agent action are defined by using standard Lightning types.

Input:

- `checkInDate`, `checkOutDate`, and `city` use standard Lightning types such as lightning\_\_dateType and lightning\_\_textType.

Output:

- The output `hotels` for the agent action is a list type.

Here’s an image that shows the custom agent action created.

![Input and output settings for a 'Find hotels' agent action. Inputs: checkInDate, checkOutDate, City. Output: hotels.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/hotel-update.png)

The available flight information is retrieved by using `@apexClassType/c__Hotel` in the agent action output, where:

- `apexClassType` is the bundle name.
- `Hotel` is the Apex class.

When you execute this agent action, it prompts you to provide input and then generates the output.

## Agent Action Execution Input

The agent’s action UI collects these details to find available hotels.

- Check in date
- Check out date
- City

Here’s the image that shows how the custom agent action input appears in an agent conversation.

![Agent action input collects hotel details: checkInDate, checkOutDate, and city.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/Example-Execution-Hotel-Input.png)

## Agent Action Execution Output

The agent’s action UI returns the available hotel details.

Here’s the image that shows how the custom agent action’s output appears in an agent conversation.

![Agent's response to a hotel details request. The response lacks labels and is presented in a format that is hard to understand.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/Example-Execution-Hotel-Output.png)

## Result Data

The agent displays the hotel data in the response.

Here’s the sample code that shows the available hotel data.

```json
{
  "hotels": [
    {
      "rooms": [
        {
          "type": "DELUX",
          "price": 2000,
          "petAllowed": false,
          "discountPercentage": 15.15,
          "available": 2
        }
      ],
      "name": "Sahara Hotels",
      "hotelCategory": {
        "star": "four"
      },
      "address": "Gacchibowli Hyderabad"
    },
    {
      "rooms": [
        {
          "type": "DELUX",
          "price": 2000,
          "petAllowed": false,
          "discountPercentage": 15.15,
          "available": 2
        }
      ],
      "name": "Taj Vivanta",
      "hotelCategory": {
        "star": "five"
      },
      "address": "Kokapet"
    }
  ]
}
```

## Customize UI for Output

Create a custom Lightning type named `hotelResponse` to enhance the visibility of the information in the output UI.

### Override Default UI for Output With Custom Lightning Types

Override the agent’s action UI for output to enhance the user experience by using Custom Lightning Types (CLTs). With CLTs, you can add your own Lightning Web Components (LWC) to present data for lists in a more structured and intuitive format.

Configure the `renderer.json` file to override the default UI of a custom Lightning type in the agent action.

Here’s an example showing a lightningTypes folder for a custom Lightning type named `hotelResponse`.

```
+--lightningTypes
        +--hotelResponse
            +--schema.json
            +--lightningDesktopGenAi
               +--renderer.json
```

:::note
This example uses `lightningDesktopGenAi` to configure the custom Lightning type. To configure the type for the `enhancedWebChat` channel, create the `renderer.json` file in the corresponding channel folder.
:::

This image shows an example of the `hotelResponse` folder structure.

![The hotelResponse folder contains schema.json and the enhancedWebChat and lightningDesktopGenAi folders. Each channel folder contains a renderer.json file.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/output-folder-hotel.png)

The custom Lightning type `hotelResponse` includes a `schema.json` file and a `renderer.json` file. The `renderer.json` file controls how the data is displayed to the user in the agent action output.

This sample code shows the contents of the `schema.json file`.

```json
{
  "title": "Hotel Reservation",
  "description": "Hotel Reservation",
  "lightning:type": "@apexClassType/c__Hotel"
}
```

This sample code shows the contents of the `renderer.json` file.

```json
{
  "collection": {
    "renderer": {
      "componentOverrides": {
        "$": {
          "definition": "c/hotelDetails"
        }
      }
    }
  }
}
```

### Build Output Components with Lightning Web Components

This section explains how the components are created and deployed for agent action output.

This image shows the Lightning Web Component (LWC) folder structure.

![The lwc folder contains a folder named hotelDetails, which is the LWC component. The hotelDetails folder includes CSS, HTML, JS, and metadata files.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/Example2-Output-LWC.png)

The LWC component includes HTML markup designed to accept output for `@apexClassType/c__Hotel`. This HTML markup ensures that the data is displayed in an intuitive and customized format.

This sample code shows the contents of the `hotelDetails.js-meta.xml` file.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>64.0</apiVersion>
    <isExposed>true</isExposed>
    <masterLabel>HotelDetails</masterLabel>
  <targets>
        <target>lightning__AgentforceOutput</target>
    </targets>
    <targetConfigs>
        <targetConfig targets="lightning__AgentforceOutput">
            <sourceType name="lightning__listType" itemTypeName="c__hotelResponse"/>
        </targetConfig>
    </targetConfigs>
</LightningComponentBundle>
```

:::note
When you create an LWC component to override the UI for action input, use `lightning__AgentforceInput` as the target. For output, use `lightning__AgentforceOutput`. For information about LWC target types, see [`lightning__AgentforceInput` Target](https://developer.salesforce.com/docs/platform/lwc/guide/targets-lightning-agentforce-input.md) and [`lightning__AgentforceOutput` Target](https://developer.salesforce.com/docs/platform/lwc/guide/targets-lightning-agentforce-output.md).
:::

This sample code shows the contents of the `hotelDetails.html` file.

```html
<template>
  <lightning-card title="Available Hotels" icon-name="standard:travel_mode">
    <template if:true="{value}">
      <div class="slds-p-around_medium">
        <template for:each="{value}" for:item="hotel">
          <div key="{hotel.name}" class="hotel-card slds-box slds-box_x-small slds-m-bottom_large">
            <div class="slds-grid slds-grid_align-spread slds-m-bottom_small">
              <div>
                <h2 class="slds-text-heading_medium slds-truncate hotel-name">{hotel.name}</h2>
                <div class="slds-text-body_small slds-m-top_xx-small slds-text-color_weak">
                  <lightning-icon
                    icon-name="utility:location"
                    size="xx-small"
                    class="slds-m-right_xx-small"
                  ></lightning-icon>
                  {hotel.address}
                </div>
              </div>
            </div>

            <div class="slds-grid slds-wrap slds-m-bottom_small">
              <template for:each="{hotel.rooms}" for:item="room">
                <div
                  key="{room.type}"
                  class="slds-box slds-box_xx-small slds-theme_shade slds-m-bottom_medium slds-size_1-of-1 room-box"
                >
                  <div class="slds-grid slds-grid_align-spread slds-m-bottom_x-small">
                    <div>
                      <p class="slds-text-title_bold">{room.type}</p>
                      <p class="slds-text-body_small">
                        <lightning-icon
                          icon-name="utility:event"
                          size="xx-small"
                          class="slds-m-right_xx-small"
                        ></lightning-icon>
                        Available: {room.available}
                      </p>
                      <p class="slds-text-body_small">
                        <lightning-icon
                          icon-name="utility:animal_and_nature"
                          size="xx-small"
                          class="slds-m-right_xx-small"
                        ></lightning-icon>
                        Pets Allowed: {room.petAllowed}
                      </p>
                    </div>
                    <div class="slds-text-align_right">
                      <div class="price-tag">₹{room.price}</div>
                      <div class="discount-chip">{room.discountPercentage}% Off</div>
                    </div>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </template>
      </div>
    </template>
  </lightning-card>
</template>
```

This sample code shows the contents of the `hotelDetails.js` file.

```js
import { LightningElement, api } from "lwc";

export default class HotelDetails extends LightningElement {
  @api value;
}
```

**See Also**

- *Lightning Web Components Developer Guide*: [Get Started with Lightning Web Components](https://developer.salesforce.com/docs/platform/lwc/guide)

### Configure Custom Lightning Type for Output in Agent Script

After you create a custom Lightning type and Lightning Web Component, configure the agent action to use them.

1. In **Agentforce Builder**, open your agent.
2. In the **Explorer** panel, go to your subagent and select the **Find hotels** action.
3. Switch to **Script** mode using the toggle at the top of the canvas.
4. Locate the `filters` output parameter in the action configuration
5. Replace the existing value of the `complex_data_type_name` property ‌with `c__hotelResponse`. Custom Lightning types use the `c__` namespace prefix.
6. Click **Save**.

:::note
The script will fail validation if you specify a non-existent custom Lightning type name.
:::

Here's an image that shows the custom Lightning type configured in Script mode:

![The agent action outputs parameter with 'c\_\_hotelResponse' selected in the complex_data_type_name property.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/hotel-output.png)

**See Also**

- [Agent Script Reference: Actions](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-ref-actions.md#outputs)

## Test, Commit, and Activate Your Agent

After you configure the custom Lightning types for output in the agent script, preview the conversation to verify the user experience. Once you're satisfied with the customized UIs, commit and activate your agent to make it available to users.

1. In **Agentforce Builder**, click the **Preview** tab.

2. Enter a test utterance, such as "Find hotels."

3. When the agent prompts for details, enter the input and review the agent's final response to verify that the hotel data renders using your custom `hotelResponse` LWC cards.

   This image shows how the custom agent action’s output appears in an agent conversation.

   ![Agent's response to a hotel details request. The response includes clear labels and is presented in a format that is easy to understand.](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/lightning-types-images/example2-output.png)

4. At the top of the canvas, click **Commit Version** and then click **Commit** to confirm.

   :::note
   To make further changes after this point, you must create a new draft from the committed version.
   :::

5. With the committed version selected, click **Activate** and confirm the activation to make the agent available to users. The currently active version (if any) is automatically deactivated.

**See Also**

- [Explore Agentforce Builder](https://help.salesforce.com/s/articleView?id=ai.agent_builder_tour.htm\&type=5)
- [Commit an Agent Version](https://help.salesforce.com/s/articleView?id=ai.agent_versions_commit.htm\&type=5)
- [Activate or Deactivate Your Agent](https://help.salesforce.com/s/articleView?id=ai.copilot_setup_activate_deactivate.htm\&type=5)
