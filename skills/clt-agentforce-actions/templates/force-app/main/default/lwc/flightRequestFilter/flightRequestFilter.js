import { api, LightningElement } from "lwc";

export default class FlightRequestFilter extends LightningElement {
  // Set by the chat panel (e.g. true after the user submits).
  @api readOnly = false;

  // Capture-only: the agent can't pre-populate this. The framework sends what the user
  // entered (via valuechange) to the action when the user submits.
  @api value;

  price;
  discountPercentage;

  connectedCallback() {
    this.price = this.value?.price ?? "";
    this.discountPercentage = this.value?.discountPercentage ?? "";
  }

  handleInputChange(event) {
    event.stopPropagation();
    const { name, value } = event.target;
    this[name] = value;
    this.dispatchEvent(
      new CustomEvent("valuechange", {
        detail: {
          value: {
            price: this.price === "" ? null : Number(this.price),
            discountPercentage: this.discountPercentage === "" ? null : Number(this.discountPercentage)
          }
        }
      })
    );
  }
}
