global class FlightAgent {

    @InvocableMethod(label='Find Flights' description='Finds available flights')
    global static List<FlightResponse> findFlights(List<FlightRequest> req) {
        // Sample data. In a real action, call your service and build the response from it.
        List<Flight> flights = new List<Flight>{
            new Flight('IX 2814', 1, false, 1000L, 20.20d, 70),
            new Flight('6E 488', 2, false, 2000L, 15.15d, 120),
            new Flight('6E 523', 1, false, 3000L, 13.14d, 75),
            new Flight('6E 6166', 2, false, 4000L, 14.14d, 130)
        };
        AvailableFlight availableFlights = new AvailableFlight();
        availableFlights.flights = flights;

        FlightResponse fr = new FlightResponse();
        fr.aFlight = availableFlights;
        return new List<FlightResponse>{ fr };
    }

    // Invocable request/response wrappers. These are not referenced by a Lightning type;
    // the classes they carry (FlightRequestFilter, AvailableFlight) are, and are top-level.
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
