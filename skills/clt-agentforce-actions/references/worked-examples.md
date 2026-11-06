# Worked examples (from the Agentforce Developer Guide)

Two complete builds. Example 1 is in [`templates/`](../templates/README.md), ready to deploy.

---

## Example 1: Flight search (top-level editor + top-level renderer)

**Goal:** the Find Flights action collects price/discount filters through a custom form (input
CLT `flightFilter`) and shows the results as flight cards (output CLT `flightResponse`).

### Apex

| Class | Role | Notes |
|---|---|---|
| `FlightAgent` | `@InvocableMethod(label='Find Flights')` + inner `FlightRequest` / `FlightResponse` wrappers (`@InvocableVariable`) | The action is created from this method |
| `AvailableFlight` | Output object: `@AuraEnabled global List<Flight> flights` | Backs `flightResponse` |
| `Flight` | `flightId` (String), `numLayovers` (Integer), `isPetAllowed` (Boolean), `price` (Long), `discountPercentage` (Double), `durationInMin` (Integer) | Item class |
| `FlightRequestFilter` | Input object: `price` (Long), `discountPercentage` (Double) | Backs `flightFilter` |

Every class is `global` and has `@JsonAccess(serializable='always' deserializable='always')`.
CLT-backed fields are `@AuraEnabled`.

Default output data (before the CLT):
```json
{ "aFlight": { "flights": [ { "flightId": "IX 2814", "price": 1000, "numLayovers": 1,
  "isPetAllowed": false, "durationInMin": 70, "discountPercentage": 20.2 } ] } }
```

### Bundles

```
lightningTypes/
  flightResponse/
    schema.json                       {"title":"My Flight Response","description":"My Flight Response","lightning:type":"@apexClassType/c__AvailableFlight"}
    lightningDesktopGenAi/renderer.json   {"renderer":{"componentOverrides":{"$":{"definition":"c/flightDetails"}}}}
    enhancedWebChat/renderer.json         (same, if Service agent)
  flightFilter/
    schema.json                       {"title":"Flight Filter","description":"Flight Filter","lightning:type":"@apexClassType/c__FlightRequestFilter"}
    lightningDesktopGenAi/editor.json     {"editor":{"componentOverrides":{"$":{"definition":"c/flightRequestFilter"}}}}
    enhancedWebChat/editor.json           (same, if Service agent)
```

### LWCs

- `flightDetails` (renderer, `lightning__AgentforceOutput`, `<sourceType name="c__flightResponse"/>`):
  in `connectedCallback`, it maps `this.value?.flights` into display rows (pets "Yes"/"No",
  minutes → "1 hr 10 min", computed arrival time), then renders a `lightning-card` per flight.
- `flightRequestFilter` (editor, `lightning__AgentforceInput`, `<targetType name="c__flightFilter"/>`):
  two `lightning-input type="number"` fields (price 1,000–20,000, discount 0–100) bound to
  `read-only={readOnly}`. `handleInputChange` calls `stopPropagation()` and dispatches `valuechange`
  with `{ price, discountPercentage }`.

### Agent

1. Agentforce Studio → new Employee or Service agent ("Flight Search Agent") → subagent "Flight
   Search" → action "Find Flights", Reference Action Type **Apex**, method **Find Flights**.
2. Script mode: `is_user_input: True` on each user-provided input. Set
   `complex_data_type_name: "c__flightFilter"` on `filters` and `"c__flightResponse"` on
   `aFlight` (`is_displayable: True`). The full action block is in
   [apex-and-actions.md](apex-and-actions.md#agent-script).
3. Instructions: *"When a customer asks about flight availability or wants to search for
   flights, use the {!@actions.Find_Flights} action. Collect the origin city, destination city,
   and date of travel from the customer before running the action."*
4. Router: `go_to_Flight_Search: @utils.transition to @subagent.Flight_Search`.
5. Preview "Find flights" → the filter form appears → submit → the flight cards render. Commit, then Activate.

---

## Example 2: Hotel search (collection renderer)

**Goal:** Find hotels returns `List<Hotel>`. One LWC renders the whole list as hotel cards with
their rooms.

### Apex (all `global`, all `@JsonAccess(serializable='always' deserializable='always')`)

```apex
global class HotelReservation {
    @InvocableMethod(label='Find hotels ' description='Find Available Hotels')
    global static List<HotelResponse> findHotels(List<HotelRequest> req) {
        Room r1 = new Room('DELUX', 2, 15.15d, 2000l, false);
        List<Room> rooms = new List<Room>{ r1 };
        List<Hotel> hotels = new List<Hotel>{
            new Hotel('Sahara Hotels', 'Gacchibowli Hyderabad', rooms, new HotelCategory('four')),
            new Hotel('Taj Vivanta', 'Kokapet', rooms, new HotelCategory('five'))
        };
        return new List<HotelResponse>{ new HotelResponse(hotels) };
    }
}
global class HotelResponse { @InvocableVariable global List<Hotel> hotels; /* ctor */ }
global class Hotel { @InvocableVariable global String name; @InvocableVariable global String address;
                     @InvocableVariable global List<Room> rooms; @InvocableVariable global HotelCategory hotelCategory; /* ctor */ }
global class Room { @InvocableVariable global String type; @InvocableVariable global Integer available;
                    @InvocableVariable global Double discountPercentage; @InvocableVariable global Long price;
                    @InvocableVariable global Boolean petAllowed; /* ctor */ }
global class HotelCategory { @InvocableVariable global String star; /* ctor */ }
global class HotelRequest { @InvocableVariable global String city;
                            @InvocableVariable global Date checkInDate; @InvocableVariable global Date checkOutDate; }
```

The docs use `@InvocableVariable` only. The Apex requirements page asks for `@AuraEnabled` on
CLT-projected fields, so add `@AuraEnabled` too when you build it.

### Bundle

```
lightningTypes/hotelResponse/
  schema.json                          {"title":"Hotel Reservation","description":"Hotel Reservation","lightning:type":"@apexClassType/c__Hotel"}
  lightningDesktopGenAi/renderer.json  ↓
  enhancedWebChat/renderer.json        (same)
```
```json
{ "collection": { "renderer": { "componentOverrides": { "$": { "definition": "c/hotelDetails" } } } } }
```

### LWC `hotelDetails`

```xml
<targets><target>lightning__AgentforceOutput</target></targets>
<targetConfigs>
  <targetConfig targets="lightning__AgentforceOutput">
    <sourceType name="lightning__listType" itemTypeName="c__hotelResponse"/>
  </targetConfig>
</targetConfigs>
```
```js
import { LightningElement, api } from "lwc";
export default class HotelDetails extends LightningElement { @api value; }   // value = Hotel[]
```
```html
<template>
  <lightning-card title="Available Hotels" icon-name="standard:travel_mode">
    <template if:true={value}>
      <div class="slds-p-around_medium">
        <template for:each={value} for:item="hotel">
          <div key={hotel.name} class="slds-box slds-box_x-small slds-m-bottom_large">
            <h2 class="slds-text-heading_medium">{hotel.name}</h2>
            <p class="slds-text-body_small slds-text-color_weak">{hotel.address}</p>
            <template for:each={hotel.rooms} for:item="room">
              <div key={room.type} class="slds-box slds-box_xx-small slds-theme_shade slds-m-top_small">
                <p class="slds-text-title_bold">{room.type}</p>
                <p>Available: {room.available} · Pets allowed: {room.petAllowed}</p>
                <p>₹{room.price} · {room.discountPercentage}% off</p>
              </div>
            </template>
          </div>
        </template>
      </div>
    </template>
  </lightning-card>
</template>
```

The docs write the template bindings as `"{value}"` (quoted). LWC templates need unquoted
`{value}`, as above.

### Agent

```agentscript
            outputs:
                hotels: list[object]
                    label: "hotels"
                    complex_data_type_name: "c__hotelResponse"     # was "@apexClassType/c__Hotel"
                    is_displayable: True
                    filter_from_agent: False
                    description: "result"
```
Inputs: `checkInDate` / `checkOutDate` as `object` with `complex_data_type_name: "lightning__dateType"`,
and `city: string`. All have `is_user_input: True`. The router transition is
`go_to_Hotel_Search: @utils.transition to @subagent.Hotel_Search`.
