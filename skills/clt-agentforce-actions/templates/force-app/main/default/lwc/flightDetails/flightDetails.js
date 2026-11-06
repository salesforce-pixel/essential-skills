import { LightningElement, api } from "lwc";

const DEPARTURE = { hours: 7, minutes: 0 }; // sample departure time; the Apex has none

export default class FlightDetails extends LightningElement {
  // Set by the framework to the AvailableFlight output: { flights: [ { flightId, price, ... } ] }
  @api value;

  get flightData() {
    const flights = this.value?.flights || [];
    return flights.map((flight) => ({
      ...flight,
      petAllowedStatus: flight.isPetAllowed ? "Yes" : "No",
      durationInHr: this.formatDuration(flight.durationInMin),
      departureTime: this.formatTime(DEPARTURE.hours * 60 + DEPARTURE.minutes),
      arrivalInHr: this.formatTime(DEPARTURE.hours * 60 + DEPARTURE.minutes + (flight.durationInMin || 0))
    }));
  }

  get hasFlights() {
    return this.flightData.length > 0;
  }

  formatDuration(durationInMin) {
    if (!durationInMin) return "";
    return `${Math.floor(durationInMin / 60)} hr ${durationInMin % 60} min`;
  }

  formatTime(totalMinutes) {
    const h = String(Math.floor(totalMinutes / 60) % 24).padStart(2, "0");
    const m = String(totalMinutes % 60).padStart(2, "0");
    return `${h}:${m}`;
  }

  // Enables the chat "copy" button for this component (global copy).
  @api
  getFormattedValue() {
    return this.flightData
      .map((f) => `${f.flightId}: $${f.price}, ${f.discountPercentage}% off, ${f.durationInHr}, layovers ${f.numLayovers}`)
      .join("\n");
  }
}
