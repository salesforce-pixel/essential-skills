@IsTest
private class FlightAgentTest {

    @IsTest
    static void findFlightsReturnsFlights() {
        FlightAgent.FlightRequest req = new FlightAgent.FlightRequest();
        req.originCity = 'Hyderabad';
        req.destinationCity = 'Delhi';
        req.dateOfTravel = Date.today().addDays(7);
        req.filters = new FlightRequestFilter();
        req.filters.price = 5000L;
        req.filters.discountPercentage = 10;

        Test.startTest();
        List<FlightAgent.FlightResponse> res = FlightAgent.findFlights(
            new List<FlightAgent.FlightRequest>{ req });
        Test.stopTest();

        Assert.areEqual(1, res.size(), 'One response per request');
        Assert.isNotNull(res[0].aFlight, 'Response carries AvailableFlight');
        Assert.areEqual(4, res[0].aFlight.flights.size(), 'Sample data has four flights');
        Assert.areEqual('IX 2814', res[0].aFlight.flights[0].flightId);
    }
}
