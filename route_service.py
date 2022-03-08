#!/usr/bin/env python3
import json
import logging
import os
from enum import Enum
from typing import Optional, List, Dict, Set, Union

import requests
from requests.adapters import HTTPAdapter, Retry


###
# Generic Abstract Classes
###
class Route:
    __slots__ = ("id", "stops")

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.id)

    def __init__(self, route_id: Union[int, str]):
        self.id = route_id
        self.stops: Set[Stop] = set()

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"

    def __str__(self):
        return str(self.id)


class Stop:
    __slots__ = ("id", "routes", "stops")

    def __eq__(self, other):
        return isinstance(other, self.__class__) and hash(self) == hash(other)

    def __hash__(self):
        return hash(self.id)

    def __init__(self, stop_id: Union[int, str]):
        self.id: Union[int, str] = stop_id
        self.routes: Set[Route] = set()

    def __repr__(self):
        return f"{self.__class__}({self})"

    def __str__(self):
        return str(self.id)


class RouteService:
    _logger = logging.Logger("RouteService")

    @property
    def routes(self) -> Set[Route]:
        raise NotImplementedError

    @property
    def stops(self) -> Set[Stop]:
        raise NotImplementedError

    def route(self, route: Union[int, str, None] = None) -> Optional[Route]:
        raise NotImplementedError

    def stop(self, stop: Union[int, str, None] = None) -> Optional[Stop]:
        raise NotImplementedError

    def trip(self, here: Stop, there: Stop) -> List[Route]:
        self._logger.info(f"{here} -> {there}")
        if isinstance(here, Stop) and isinstance(there, Stop):
            self._logger.info(f"Here line routes: {','.join(str(r) for r in here.routes)}")
            self._logger.info(f"There line routes: {','.join(str(r) for r in there.routes)}")

            routes = []
            for route in here.routes:
                trip = self.__create_trip(route, there)
                if trip:
                    routes.append(trip)
            routes.sort(key=lambda r: len(r))
            if routes:
                return routes[0]
        return []

    def __create_trip(self, looking: Route, destination: Stop, visited: Optional[List[Route]] = None) -> List[Route]:
        if visited is not None:
            visit_and_look = visited + [looking]
        else:
            visit_and_look = [looking]
        if destination in looking.stops:
            return visit_and_look
        trips = []
        for stop in looking.stops:
            for route in stop.routes:
                if route not in visit_and_look:
                    to_destination = self.__create_trip(route, destination, visit_and_look)
                    if to_destination:
                        trips.append(to_destination)
        if trips:
            trips.sort(key=lambda t: len(t))
            return trips[0]
        return []


class RouteServiceException(Exception):
    pass


class RouteServiceHttpException(RouteServiceException):
    pass


class RouteServiceJsonException(RouteServiceException):
    pass


###
# MBTA Specific implementations
###
class MBTARoute(Route):
    """
    {
      "type": "string",
      "relationships": {},
      "links": {},
      "id": "string",
      "attributes": {
        "type": 1,
        "text_color": "000000",
        "sort_order": 0,
        "short_name": "Red",
        "long_name": "Red Line",
        "fare_class": "Free",
        "direction_names": [
          "string"
        ],
        "direction_destinations": [
          "string"
        ],
        "description": "Rapid Transit",
        "color": "FFFFFF"
      }
    }
    """
    __slots__ = ("type", "relationships", "links", "short_name", "long_name", "fare_class", "direction_names", "direction_destinations", "description", "color")

    def __init__(self, json_source):
        super(MBTARoute, self).__init__(json_source["id"])

        self.type = json_source["type"]
        self.relationships = json_source["relationships"]
        self.links = json_source["links"]
        self.type = json_source["attributes"]["type"]
        self.short_name = json_source["attributes"]["short_name"]
        self.long_name = json_source["attributes"]["long_name"]
        self.fare_class = json_source["attributes"]["fare_class"]
        self.direction_names = json_source["attributes"]["direction_names"]
        self.direction_destinations = json_source["attributes"]["direction_destinations"]
        self.description = json_source["attributes"]["description"]
        self.color = json_source["attributes"]["color"]

    def __str__(self):
        return self.long_name


class MBTAStop(Stop):
    """
    {
      "type": "string",
      "relationships": {
        "parent_station": {
          "links": {
            "self": "string",
            "related": "string"
          },
          "data": {
            "type": "string",
            "id": "string"
          }
        }
      },
      "links": {},
      "id": "string",
      "attributes": {
        "wheelchair_boarding": 0,
        "vehicle_type": 3,
        "platform_name": "Red Line",
        "platform_code": "5",
        "on_street": "Massachusetts Avenue",
        "name": "Parker St @ Hagen Rd",
        "municipality": "Cambridge",
        "longitude": 42.316115,
        "location_type": 0,
        "latitude": -71.194994,
        "description": "Alewife - Red Line",
        "at_street": "Essex Street",
        "address": "Alewife Brook Parkway and Cambridge Park Drive, Cambridge, MA 02140"
      }
    }
    """

    __slots__ = (
        "type", "relationships", "links", "address", "at_street", "description", "longitude", "location_type",
        "latitude", "municipality", "name", "platform_name", "platform_code", "vehicle_type", "wheelchair_boarding"
    )

    def __init__(self, json_source):
        super(MBTAStop, self).__init__(json_source["id"])
        self.type = json_source["type"]
        self.relationships = json_source["relationships"]
        self.links = json_source["links"]

        self.address = json_source["attributes"]["address"]
        self.at_street = json_source["attributes"]["at_street"]
        self.description = json_source["attributes"]["description"]
        self.longitude = json_source["attributes"]["longitude"]
        self.location_type = json_source["attributes"]["location_type"]
        self.latitude = json_source["attributes"]["latitude"]
        self.municipality = json_source["attributes"]["municipality"]
        self.name = json_source["attributes"]["name"]
        self.platform_name = json_source["attributes"]["platform_name"]
        self.platform_code = json_source["attributes"]["platform_code"]
        self.vehicle_type = json_source["attributes"]["vehicle_type"]
        self.wheelchair_boarding = json_source["attributes"]["wheelchair_boarding"]

        self.routes = set()

    def __str__(self):
        return self.name


class RouteTypes(Enum):
    """
0 - Tram, Streetcar, Light rail. Any light rail or street level system within a metropolitan area.
1 - Subway, Metro. Any underground rail system within a metropolitan area.
2 - Rail. Used for intercity or long-distance travel.
3 - Bus. Used for short- and long-distance bus routes.
4 - Ferry. Used for short- and long-distance boat service.
5 - Cable tram. Used for street-level rail cars where the cable runs beneath the vehicle (e.g., cable car in San Francisco).
6 - Aerial lift, suspended cable car (e.g., gondola lift, aerial tramway). Cable transport where cabins, cars, gondolas or open chairs are suspended by means of one or more cables.
7 - Funicular. Any rail system designed for steep inclines.
11 - Trolleybus. Electric buses that draw power from overhead wires using poles.
12 - Monorail. Railway in which the track consists of a single rail or a beam.
    """
    LIGHT_RAIL = 0
    STREET_CAR = LIGHT_RAIL
    TRAM = LIGHT_RAIL
    SUBWAY = 1
    METRO = SUBWAY
    RAIL = 2
    BUS = 3
    FERRY = 4
    CABLE_TRAM = 5
    AERIAL_LIFT = 6
    FUNICULAR = 7
    TROLLEY_BUS = 11
    MONORAIL = 12


class MBTARouteService(RouteService):
    _logger = logging.Logger("RouteService.MBTA")

    base_url = "https://api-v3.mbta.com"
    route_path = "/routes"
    stop_path = "/stops"

    def __init__(self, api_key: Optional[str] = None, route_types: List[RouteTypes] = None):
        self._session = requests.Session()
        _adapter = HTTPAdapter(max_retries=Retry(
            total=5,
            backoff_factor=2.0,  # {backoff_factor} * (2 ** ({number of total retries} - 1))
            allowed_methods=frozenset(["GET"]),
            respect_retry_after_header=True,
            status_forcelist=frozenset({429}),
        ))
        self._session.mount("http://", _adapter)
        self._session.mount("https://", _adapter)
        # Set the headers for the entire session
        if api_key is not None:
            self._session.headers = {"x-api-key": api_key}

        if route_types is None:
            self._route_types = []
        else:
            self._route_types = route_types
        self.__routes: Optional[Dict[Union[int, str], MBTARoute]] = None
        self.__stops: Optional[Dict[Union[int, str], MBTAStop]] = None

    @property
    def routes(self) -> Set[MBTARoute]:
        if self.__routes is None:
            self.__get_routes_and_stops()
        return set(self.__routes.values())

    @property
    def stops(self) -> Set[MBTAStop]:
        if self.__stops is None:
            self.__get_routes_and_stops()
        return set(self.__stops.values())

    def route(self, route: Union[int, str, None] = None) -> Optional[MBTARoute]:
        if self.routes:
            return self.__routes.get(str(route).casefold(), None)  # allow case-insensitive matching
        else:
            return None

    def stop(self, stop: Union[int, str, None] = None) -> Optional[MBTAStop]:
        if self.stops:
            return self.__stops.get(str(stop).casefold(), None)  # allow case-insensitive matching
        else:
            return None

    def __get_routes_and_stops(self):
        route_type_parameters = ",".join(str(t.value) for t in self._route_types)
        self.__routes = {}
        self.__stops = {}
        try:
            with self._session.get(f"{self.base_url}{self.route_path}", params={"filter[type]": route_type_parameters}) as response:
                self._logger.info(response.request.url)
                response.raise_for_status()
                self._logger.debug(json.dumps(response.json(), indent=2))
                for route in response.json()["data"]:
                    mbta_route = MBTARoute(route)
                    self.__routes[mbta_route.id] = mbta_route
                    self.__routes[str(mbta_route).casefold()] = mbta_route
                    try:
                        with self._session.get(f"{self.base_url}{self.stop_path}", params={"filter[route]": mbta_route.id}) as stop_response:
                            self._logger.info(stop_response.request.url)
                            stop_response.raise_for_status()
                            self._logger.debug(json.dumps(stop_response.json(), indent=2))
                            for stop in stop_response.json()["data"]:
                                try:
                                    mbta_stop = self.__stops[stop["id"]]
                                except KeyError:
                                    mbta_stop = MBTAStop(stop)
                                    self.__stops[mbta_stop.id] = mbta_stop
                                    self.__stops[str(mbta_stop).casefold()] = mbta_stop
                                mbta_route.stops.add(mbta_stop)
                                mbta_stop.routes.add(mbta_route)
                    except KeyError as e:
                        self._logger.warning("Received malformed JSON from stop request")
                        raise RouteServiceJsonException(e)
        except requests.exceptions.HTTPError as e:
            self._logger.warning(e)
            raise RouteServiceHttpException(e)
        except KeyError as e:
            self._logger.warning("Received malformed JSON from route request")
            raise RouteServiceJsonException(e)


###
# TUI Client Implementation
###
def list_stops(route_service: RouteService, *_unused_args):
    if route_service.stops:
        stop_label_size = max(len(str(stop)) for stop in route_service.stops) + 4
        stops_per_line = 120 // stop_label_size
        print("Stops:")
        for index, stop in enumerate(route_service.stops):
            output = f'{str(stop): >{stop_label_size}}'
            if index % stops_per_line < stops_per_line - 1:
                print(output, end="")
            else:
                print(output)
    else:
        print(f"No known stops")
    print()


def one(route_service: RouteService, *_unused_args):
    """
    Question 1
    Write a program that retrieves data representing all, what we'll call "subway" routes: "Light Rail" (type 0) and “Heavy Rail” (type 1). The program should list their “long names” on the console.
    Partial example of long name output: Red Line, Blue Line, Orange Line...
    There are two ways to filter results for subway-only routes. Think about the two options below
    and choose:
    1. Download all results from https://api-v3.mbta.com/routesthenfilterlocally
    2. Rely on the server API (i.e., https://api-v3.mbta.com/routes?filter[type]=0,1) to filter before results are received
    Please document your decision and your reasons for it.

    Hint: It might be tempting to hardcode things in your algorithm that are specific to the MBTA system, but we believe it will make things easier for you to generalize your solution so that it could work for different and/or larger subway systems.
    How you handle input, represent train routes, and present output is your choice.
    """
    if route_service.routes:
        print("Routes:")
        for route in route_service.routes:
            print(f"  {route}")
    else:
        print("No known routes!")


def two(route_service: RouteService, *_unused_args):
    """
    Question 2
    Extend your program such that it displays the following additional information.
    1. The name of the subway route with the most stops as well as a count of its stops.
    2. The name of the subway route with the fewest stops as well as a count of its stops.
    3. A list of the stops that connect two or more subway routes along with the relevant route
    names for each of those stops.

    Hint: It might be tempting to hardcode things in your algorithm that are specific to the MBTA system, but we believe it will make things easier for you to generalize your solution so that it could work for different and/or larger subway systems.
    How you handle input, represent train routes, and present output is your choice.
    """
    one(route_service)
    if route_service.routes:
        sorted_routes = sorted(route_service.routes, key=lambda r: len(r.stops))
        print(f"Route with the Fewest Stops: {sorted_routes[0]} ({len(sorted_routes[0].stops)})")
        print(f"Route with the Most Stops: {sorted_routes[-1]} ({len(sorted_routes[-1].stops)})")
        print("Stops with Multiple Routes:")
        for stop in (s for s in route_service.stops if len(s.routes) >= 2):
            print(f"  {stop}: {', '.join(str(r) for r in stop.routes)}")


def three(route_service: RouteService, start: Optional[str] = None, destination: Optional[str] = None, interactive: bool = False, *_unused_args):
    """
    Question 3
    Extend your program again such that the user can provide any two stops on the subway routes you listed for question 1.
    List a rail route you could travel to get from one stop to the other. We will not evaluate your solution based upon the efficiency or cleverness of your route-finding solution. Pick a simple solution that answers the question.
    We will want you to understand and be able to explain how your algorithm performs.
    Examples:
    1. Davis to Kendall -> Redline
    2. Ashmont to Arlington -> Redline, Greenline

    Hint: It might be tempting to hardcode things in your algorithm that are specific to the MBTA system, but we believe it will make things easier for you to generalize your solution so that it could work for different and/or larger subway systems.
    How you handle input, represent train routes, and present output is your choice.
    """

    # Turn strings into stops
    if start is not None and destination is not None:
        start = start.strip()
        destination = destination.strip()
        starting_stop = route_service.stop(start)
        destination_stop = route_service.stop(destination)
        if starting_stop is None:
            print(f'Unable to find the stop "{start}"')
        elif destination_stop is None:
            print(f'Unable to find the stop "{destination}"')
        else:
            trip = route_service.trip(starting_stop, destination_stop)
            print(f"{start} to {destination} -> {', '.join(str(t) for t in trip)}")
    while start != "" and interactive:  # This explicit check allows the first iteration
        start = input("Enter the starting stop: ").strip()  # trim white space from input
        if start == "list":
            list_stops(route_service)
        elif start != "":
            starting_stop = route_service.stop(start)
            if starting_stop is None:
                print(f'Unable to find the stop "{start}"')
            else:
                destination = input("Enter the destination stop: ").strip()  # trim white space from input
                if destination != "":
                    destination_stop = route_service.stop(destination)
                    if destination_stop is None:
                        print(f'Unable to find the stop "{destination}"')
                    else:
                        trip = route_service.trip(starting_stop, destination_stop)
                        print(f"{start} to {destination} -> {', '.join(str(t) for t in trip)}")


def main():
    ###
    # Parse command line arguments
    # Only the constructor is specific to the MBTARouteService implementation
    ###
    import argparse

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-a', '--api-key', help='specify an API Key directly, this will override the environment value for MBTA_API_KEY (if set)')
    argument_parser.add_argument('-v', '--verbose', default=0, dest='verbosity', action='count', help='be more verbose with output')
    argument_parser.add_argument('-i', '--interactive', default=False, action="store_true", help='interactive solution for question three')

    route_group = argument_parser.add_argument_group("route types")
    for route_type in RouteTypes:
        flag = route_type.name.lower().replace("_", "-")
        description = route_type.name.lower().replace("_", " ")
        route_group.add_argument(f"--{flag}", dest="route_types", action="append_const", const=route_type, help=f"include {description} routes")

    other_functions = argument_parser.add_mutually_exclusive_group()
    other_functions.add_argument("-1", "--one", dest="func", action="store_const", const=one, help="solution for question one")
    other_functions.add_argument("-2", "--two", dest="func", action="store_const", const=two, help="solution for question two")
    other_functions.add_argument('-l', '--list-stops', dest="func", action="store_const", const=list_stops, help='list the stops in this collection of routes')

    argument_parser.set_defaults(func=three)
    argument_parser.add_argument("start", nargs="?", metavar="INITIAL_STOP", help='initial stop')
    argument_parser.add_argument("destination", nargs="?", metavar="DESTINATION_STOP", help='destination stop')

    parsed_arguments = argument_parser.parse_args()

    ###
    # Configure Logging
    ###
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
    logging.getLogger().setLevel(logging.WARNING - parsed_arguments.verbosity * 10)

    if parsed_arguments.route_types:
        route_types = parsed_arguments.route_types
    else:
        route_types = [RouteTypes.LIGHT_RAIL, RouteTypes.SUBWAY]
    api_key = None
    if parsed_arguments.api_key is not None:
        api_key = parsed_arguments.api_key
    elif "MBTA_API_KEY" in os.environ:
        api_key = os.environ.get("MBTA_API_KEY")
    route_service = MBTARouteService(api_key, route_types=route_types)
    ###
    # Execute
    ###
    parsed_arguments.func(route_service, parsed_arguments.start, parsed_arguments.destination, parsed_arguments.interactive)


if __name__ == "__main__":
    main()
