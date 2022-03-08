# DSP Take Home
This is a Python implementation of the DSP Take Home Interview Exercise. All command examples assume that they will be run from within the folder containing this utility. Additionally, all command examples use `python3` (and `pip3`), but on Windows systems these commands will be `python` (and `pip`).

## Requirements
This utility requires [Python 3.6 (or greater)](https://www.python.org/downloads/) and the requests package (2.27.1 or greater).
Once a Python interpreter is installed requests may be installed by running the following command:

`pip3 install requests` or `pip3 -r requirements.txt`

## Testing
`test_route_service.py` includes a number of unit tests built using the unittest package (included with most Python 3 installs).
These tests require the responses package (used to mock requests). Once the responses package has been installed (`pip3 install responses`), the unit tests may be run with the following command:

`python3 -m unittest`

## Execution
`route_service.py` is a command line tool with a text based interface. It defaults to the more interesting solution to question 3.

It may be called directly on Linux and macOS systems (`./route_service.py`) or passed as an argument to the Python interpreter (`python3 route_service.py`).

### Question 1
To list all "subway" routes call `route_service.py` with `-1` or `--one`. This will output all "light rail" and "subway" routes (as described by MBTA) (e.g. `python3 route_service.py -1`).

### Question 2
To also display the route with the most stops, the route with the least stops, and list stops connecting more than one route call `route_service.py` with `-2` or `--two` (e.g. `python3 route_service.py -2`).

### Question 3
Determining which routes connect two stops can be done in one of two ways:
 1. Specify the stop names when calling `route_service.py` (e.g. `python3 route_service.py "Warren Street" "Fenwood Road"`). Remember that stop names containing spaces MUST be quoted or escaped.
 2. Call `route_service.py -i` and enter the stop names when prompted. Multiple pairs of stops can be evaluated in this fashion. Remember that an empty "starting stop" will quit this mode and entering "list" as the starting stop will list all available stops.
 3. Combine 1 and 2 by specifying stop names when calling `route_service.py -i` (e.g. `python3 route_service.py -i "Warren Street" "Fenwood Road"`).

### Beyond
The flags `-h` or `--help` can be used to list all options (e.g. `python3 route_serviec.py --h`). 

#### API Key
An API key may be used to reduce the likelihood of rate limiting http requests. The API key may be specified using the `-a` flag or by setting the `MBTA_API_KEY` environment variable. Rate limiting shouldn't prevent this utility from functioning, but it will slow things down dramatically.  

#### List All Stops
To list all stops call `route_service.py` with `-l` or `--list` (e.g. `python3 route_serviec.py -l`). This can be useful for the default "Question 3" solution.

#### Explore Different Route Types
The help message includes a number of route types. These may be specified in any combination to show different types of routes and their stops (e.g. `python3 route_serviec.py -l --monorail`).
