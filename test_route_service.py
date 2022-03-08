#!/usr/bin/env python3
# Copyright (c) <year> <copyright holders>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import copy
import unittest

import responses

import route_service

RED_ROUTE = {
            "attributes": {
                "color": "DA291C",
                "description": "Rapid Transit",
                "direction_destinations": [
                    "Ashmont/Braintree",
                    "Alewife"
                ],
                "direction_names": [
                    "South",
                    "North"
                ],
                "fare_class": "Rapid Transit",
                "long_name": "Red Line",
                "short_name": "",
                "sort_order": 10010,
                "text_color": "FFFFFF",
                "type": 1
            },
            "id": "Red",
            "links": {
                "self": "/routes/Red"
            },
            "relationships": {
                "line": {
                    "data": {
                        "id": "line-Red",
                        "type": "line"
                    }
                }
            },
            "type": "route"
        }
GREEN_B_ROUTE = {
            "attributes": {
                "color": "00843D",
                "description": "Rapid Transit",
                "direction_destinations": [
                    "Boston College",
                    "Government Center"
                ],
                "direction_names": [
                    "West",
                    "East"
                ],
                "fare_class": "Rapid Transit",
                "long_name": "Green Line B",
                "short_name": "B",
                "sort_order": 10032,
                "text_color": "FFFFFF",
                "type": 0
            },
            "id": "Green-B",
            "links": {
                "self": "/routes/Green-B"
            },
            "relationships": {
                "line": {
                    "data": {
                        "id": "line-Green",
                        "type": "line"
                    }
                }
            },
            "type": "route"
        }
MATTAPAN_ROUTE = {
            "attributes": {
                "color": "DA291C",
                "description": "Rapid Transit",
                "direction_destinations": [
                    "Mattapan",
                    "Ashmont"
                ],
                "direction_names": [
                    "Outbound",
                    "Inbound"
                ],
                "fare_class": "Rapid Transit",
                "long_name": "Mattapan Trolley",
                "short_name": "",
                "sort_order": 10011,
                "text_color": "FFFFFF",
                "type": 0
            },
            "id": "Mattapan",
            "links": {
                "self": "/routes/Mattapan"
            },
            "relationships": {
                "line": {
                    "data": {
                        "id": "line-Mattapan",
                        "type": "line"
                    }
                }
            },
            "type": "route"
        }
ROUTE_RESPONSE = {
    "data": [],
    "jsonapi": {
        "version": "1.0"
    }
}
GREEN_B_STOP_RESPONSE = {
    "data": [
        {
            "attributes": {
                "address": "Cambridge St and Court St, Boston, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.359705,
                "location_type": 1,
                "longitude": -71.059215,
                "municipality": "Boston",
                "name": "Government Center",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-gover",
            "links": {
                "self": "/stops/place-gover"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-gover"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Tremont St and Winter St, Boston, MA 02108",
                "at_street": None,
                "description": None,
                "latitude": 42.356395,
                "location_type": 1,
                "longitude": -71.062424,
                "municipality": "Boston",
                "name": "Park Street",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-pktrm",
            "links": {
                "self": "/stops/place-pktrm"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-pktrm"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Boylston St and Tremont St, Boston, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.35302,
                "location_type": 1,
                "longitude": -71.06459,
                "municipality": "Boston",
                "name": "Boylston",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 2
            },
            "id": "place-boyls",
            "links": {
                "self": "/stops/place-boyls"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-boyls"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Arlington St and Boylston St, Boston, MA 02116",
                "at_street": None,
                "description": None,
                "latitude": 42.351902,
                "location_type": 1,
                "longitude": -71.070893,
                "municipality": "Boston",
                "name": "Arlington",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-armnl",
            "links": {
                "self": "/stops/place-armnl"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-armnl"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Boylston St and Dartmouth St, Boston, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.349974,
                "location_type": 1,
                "longitude": -71.077447,
                "municipality": "Boston",
                "name": "Copley",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-coecl",
            "links": {
                "self": "/stops/place-coecl"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-coecl"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "100 Massachusetts Ave, Boston, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.347888,
                "location_type": 1,
                "longitude": -71.087903,
                "municipality": "Boston",
                "name": "Hynes Convention Center",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 2
            },
            "id": "place-hymnl",
            "links": {
                "self": "/stops/place-hymnl"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-hymnl"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Kenmore St, Boston, MA 02215",
                "at_street": None,
                "description": None,
                "latitude": 42.348949,
                "location_type": 1,
                "longitude": -71.095169,
                "municipality": "Boston",
                "name": "Kenmore",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-kencl",
            "links": {
                "self": "/stops/place-kencl"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-kencl"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Blandford Mall, Boston, MA 02215",
                "at_street": None,
                "description": None,
                "latitude": 42.349293,
                "location_type": 1,
                "longitude": -71.100258,
                "municipality": "Boston",
                "name": "Blandford Street",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 2
            },
            "id": "place-bland",
            "links": {
                "self": "/stops/place-bland"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-bland"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Granby St, Boston, MA 02215",
                "at_street": None,
                "description": None,
                "latitude": 42.349735,
                "location_type": 1,
                "longitude": -71.103889,
                "municipality": "Boston",
                "name": "Boston University East",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-buest",
            "links": {
                "self": "/stops/place-buest"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-buest"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Marsh Chapel, Boston, MA 02215",
                "at_street": None,
                "description": None,
                "latitude": 42.350082,
                "location_type": 1,
                "longitude": -71.106865,
                "municipality": "Boston",
                "name": "Boston University Central",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-bucen",
            "links": {
                "self": "/stops/place-bucen"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-bucen"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Amory St, Boston, MA 02215",
                "at_street": None,
                "description": None,
                "latitude": 42.350992,
                "location_type": 1,
                "longitude": -71.114748,
                "municipality": "Boston",
                "name": "Amory Street",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-amory",
            "links": {
                "self": "/stops/place-amory"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-amory"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Babcock St, Boston, MA 02215",
                "at_street": None,
                "description": None,
                "latitude": 42.351616,
                "location_type": 1,
                "longitude": -71.119924,
                "municipality": "Boston",
                "name": "Babcock Street",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-babck",
            "links": {
                "self": "/stops/place-babck"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-babck"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Brighton Ave, Boston, MA 02215",
                "at_street": None,
                "description": None,
                "latitude": 42.351967,
                "location_type": 1,
                "longitude": -71.125031,
                "municipality": "Boston",
                "name": "Packard's Corner",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 2
            },
            "id": "place-brico",
            "links": {
                "self": "/stops/place-brico"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-brico"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Harvard Ave, Boston, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.350243,
                "location_type": 1,
                "longitude": -71.131355,
                "municipality": "Boston",
                "name": "Harvard Avenue",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-harvd",
            "links": {
                "self": "/stops/place-harvd"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-harvd"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Griggs St, Boston, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.348545,
                "location_type": 1,
                "longitude": -71.134949,
                "municipality": "Boston",
                "name": "Griggs Street",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 2
            },
            "id": "place-grigg",
            "links": {
                "self": "/stops/place-grigg"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-grigg"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Allston St and Commonwealth Ave, Boston, MA 02134",
                "at_street": None,
                "description": None,
                "latitude": 42.348701,
                "location_type": 1,
                "longitude": -71.137955,
                "municipality": "Boston",
                "name": "Allston Street",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 2
            },
            "id": "place-alsgr",
            "links": {
                "self": "/stops/place-alsgr"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-alsgr"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Warren St, Boston, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.348343,
                "location_type": 1,
                "longitude": -71.140457,
                "municipality": "Boston",
                "name": "Warren Street",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 2
            },
            "id": "place-wrnst",
            "links": {
                "self": "/stops/place-wrnst"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-wrnst"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Washington St, Boston, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.343864,
                "location_type": 1,
                "longitude": -71.142853,
                "municipality": "Boston",
                "name": "Washington Street",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-wascm",
            "links": {
                "self": "/stops/place-wascm"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-wascm"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Sutherland Rd, Boston, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.341614,
                "location_type": 1,
                "longitude": -71.146202,
                "municipality": "Boston",
                "name": "Sutherland Road",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 2
            },
            "id": "place-sthld",
            "links": {
                "self": "/stops/place-sthld"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-sthld"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Chiswick Rd, Boston, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.340805,
                "location_type": 1,
                "longitude": -71.150711,
                "municipality": "Boston",
                "name": "Chiswick Road",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 2
            },
            "id": "place-chswk",
            "links": {
                "self": "/stops/place-chswk"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-chswk"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Chestnut Hill Ave, Boston, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.338169,
                "location_type": 1,
                "longitude": -71.15316,
                "municipality": "Boston",
                "name": "Chestnut Hill Avenue",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 2
            },
            "id": "place-chill",
            "links": {
                "self": "/stops/place-chill"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-chill"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": None,
                "at_street": None,
                "description": None,
                "latitude": 42.3396,
                "location_type": 1,
                "longitude": -71.157661,
                "municipality": "Boston",
                "name": "South Street",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 2
            },
            "id": "place-sougr",
            "links": {
                "self": "/stops/place-sougr"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-sougr"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Commonwealth Ave and Lake St, Boston, MA 02135",
                "at_street": None,
                "description": None,
                "latitude": 42.340081,
                "location_type": 1,
                "longitude": -71.166769,
                "municipality": "Boston",
                "name": "Boston College",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-lake",
            "links": {
                "self": "/stops/place-lake"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-lake"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        }
    ],
    "jsonapi": {
        "version": "1.0"
    }
}
MATTAPAN_STOP_RESPONSE = {
    "data": [
        {
            "attributes": {
                "address": "Dorchester Ave and Ashmont St, Boston, MA 02124",
                "at_street": None,
                "description": None,
                "latitude": 42.28452,
                "location_type": 1,
                "longitude": -71.063777,
                "municipality": "Boston",
                "name": "Ashmont",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-asmnl",
            "links": {
                "self": "/stops/place-asmnl"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-asmnl"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Fellsway St and Milton St, Dorchester, MA 02124",
                "at_street": None,
                "description": None,
                "latitude": 42.279629,
                "location_type": 1,
                "longitude": -71.060394,
                "municipality": "Boston",
                "name": "Cedar Grove",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-cedgr",
            "links": {
                "self": "/stops/place-cedgr"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-cedgr"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Butler St and Branchfield St, Dorchester, MA 02124",
                "at_street": None,
                "description": None,
                "latitude": 42.272429,
                "location_type": 1,
                "longitude": -71.062519,
                "municipality": "Boston",
                "name": "Butler",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-butlr",
            "links": {
                "self": "/stops/place-butlr"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-butlr"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "1 Adams St, Milton, MA 02186",
                "at_street": None,
                "description": None,
                "latitude": 42.270349,
                "location_type": 1,
                "longitude": -71.067266,
                "municipality": "Milton",
                "name": "Milton",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-miltt",
            "links": {
                "self": "/stops/place-miltt"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-miltt"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "23 Central Ave, Milton, MA 02186",
                "at_street": None,
                "description": None,
                "latitude": 42.270027,
                "location_type": 1,
                "longitude": -71.073444,
                "municipality": "Milton",
                "name": "Central Avenue",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-cenav",
            "links": {
                "self": "/stops/place-cenav"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-cenav"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "291 Valley Rd, Milton, MA 02186",
                "at_street": None,
                "description": None,
                "latitude": 42.268347,
                "location_type": 1,
                "longitude": -71.081343,
                "municipality": "Milton",
                "name": "Valley Road",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 2
            },
            "id": "place-valrd",
            "links": {
                "self": "/stops/place-valrd"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-valrd"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "50 Capen St, Milton, MA 02186",
                "at_street": None,
                "description": None,
                "latitude": 42.267563,
                "location_type": 1,
                "longitude": -71.087338,
                "municipality": "Milton",
                "name": "Capen Street",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-capst",
            "links": {
                "self": "/stops/place-capst"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-capst"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "500 River St, Boston, MA 02126",
                "at_street": None,
                "description": None,
                "latitude": 42.26762,
                "location_type": 1,
                "longitude": -71.092486,
                "municipality": "Boston",
                "name": "Mattapan",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-matt",
            "links": {
                "self": "/stops/place-matt"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-matt"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        }
    ],
    "jsonapi": {
        "version": "1.0"
    }
}
RED_STOP_RESPONSE = {
    "data": [
        {
            "attributes": {
                "address": "Alewife Brook Pkwy and Cambridge Park Dr, Cambridge, MA 02140",
                "at_street": None,
                "description": None,
                "latitude": 42.395428,
                "location_type": 1,
                "longitude": -71.142483,
                "municipality": "Cambridge",
                "name": "Alewife",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-alfcl",
            "links": {
                "self": "/stops/place-alfcl"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-alfcl"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "College Ave and Elm St, Somerville, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.39674,
                "location_type": 1,
                "longitude": -71.121815,
                "municipality": "Somerville",
                "name": "Davis",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-davis",
            "links": {
                "self": "/stops/place-davis"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-davis"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "1899 Massachusetts Ave, Cambridge, MA 02140",
                "at_street": None,
                "description": None,
                "latitude": 42.3884,
                "location_type": 1,
                "longitude": -71.119149,
                "municipality": "Cambridge",
                "name": "Porter",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-portr",
            "links": {
                "self": "/stops/place-portr"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-portr"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": {
                        "id": "CR-zone-1A",
                        "type": "zone"
                    }
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "1400 Massachusetts Ave, Cambridge, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.373362,
                "location_type": 1,
                "longitude": -71.118956,
                "municipality": "Cambridge",
                "name": "Harvard",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-harsq",
            "links": {
                "self": "/stops/place-harsq"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-harsq"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Massachusetts Avenue and Prospect Street, Cambridge, MA 02139",
                "at_street": None,
                "description": None,
                "latitude": 42.365486,
                "location_type": 1,
                "longitude": -71.103802,
                "municipality": "Cambridge",
                "name": "Central",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-cntsq",
            "links": {
                "self": "/stops/place-cntsq"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-cntsq"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "300 Main St, Cambridge, MA 02142",
                "at_street": None,
                "description": None,
                "latitude": 42.362491,
                "location_type": 1,
                "longitude": -71.086176,
                "municipality": "Cambridge",
                "name": "Kendall/MIT",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-knncl",
            "links": {
                "self": "/stops/place-knncl"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-knncl"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Cambridge St and Charles St, Boston, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.361166,
                "location_type": 1,
                "longitude": -71.070628,
                "municipality": "Boston",
                "name": "Charles/MGH",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-chmnl",
            "links": {
                "self": "/stops/place-chmnl"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-chmnl"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Tremont St and Winter St, Boston, MA 02108",
                "at_street": None,
                "description": None,
                "latitude": 42.356395,
                "location_type": 1,
                "longitude": -71.062424,
                "municipality": "Boston",
                "name": "Park Street",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-pktrm",
            "links": {
                "self": "/stops/place-pktrm"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-pktrm"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Washington St and Summer St, Boston, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.355518,
                "location_type": 1,
                "longitude": -71.060225,
                "municipality": "Boston",
                "name": "Downtown Crossing",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-dwnxg",
            "links": {
                "self": "/stops/place-dwnxg"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-dwnxg"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "700 Atlantic Ave, Boston, MA 02110",
                "at_street": None,
                "description": None,
                "latitude": 42.352271,
                "location_type": 1,
                "longitude": -71.055242,
                "municipality": "Boston",
                "name": "South Station",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-sstat",
            "links": {
                "self": "/stops/place-sstat"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-sstat"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": {
                        "id": "CR-zone-1A",
                        "type": "zone"
                    }
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Dorchester Ave and Broadway, Boston, MA",
                "at_street": None,
                "description": None,
                "latitude": 42.342622,
                "location_type": 1,
                "longitude": -71.056967,
                "municipality": "Boston",
                "name": "Broadway",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-brdwy",
            "links": {
                "self": "/stops/place-brdwy"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-brdwy"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Dorchester Ave and Southhampton St, South Boston, MA 02127",
                "at_street": None,
                "description": None,
                "latitude": 42.330154,
                "location_type": 1,
                "longitude": -71.057655,
                "municipality": "Boston",
                "name": "Andrew",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-andrw",
            "links": {
                "self": "/stops/place-andrw"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-andrw"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "599 Old Colony Ave Boston, MA 02127-3805",
                "at_street": None,
                "description": None,
                "latitude": 42.320685,
                "location_type": 1,
                "longitude": -71.052391,
                "municipality": "Boston",
                "name": "JFK/UMass",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-jfk",
            "links": {
                "self": "/stops/place-jfk"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-jfk"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": {
                        "id": "CR-zone-1A",
                        "type": "zone"
                    }
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "125 Savin Hill Ave, Dorchester, MA 02124",
                "at_street": None,
                "description": None,
                "latitude": 42.31129,
                "location_type": 1,
                "longitude": -71.053331,
                "municipality": "Boston",
                "name": "Savin Hill",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-shmnl",
            "links": {
                "self": "/stops/place-shmnl"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-shmnl"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "50 Freeman St, Dorchester, MA 02122",
                "at_street": None,
                "description": None,
                "latitude": 42.300093,
                "location_type": 1,
                "longitude": -71.061667,
                "municipality": "Boston",
                "name": "Fields Corner",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-fldcr",
            "links": {
                "self": "/stops/place-fldcr"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-fldcr"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Dayton St and Clementine Park, Dorchester, MA 02124",
                "at_street": None,
                "description": None,
                "latitude": 42.293126,
                "location_type": 1,
                "longitude": -71.065738,
                "municipality": "Boston",
                "name": "Shawmut",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-smmnl",
            "links": {
                "self": "/stops/place-smmnl"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-smmnl"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Dorchester Ave and Ashmont St, Boston, MA 02124",
                "at_street": None,
                "description": None,
                "latitude": 42.28452,
                "location_type": 1,
                "longitude": -71.063777,
                "municipality": "Boston",
                "name": "Ashmont",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-asmnl",
            "links": {
                "self": "/stops/place-asmnl"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-asmnl"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Hancock St and Hunt St, Quincy, MA 02171",
                "at_street": None,
                "description": None,
                "latitude": 42.275275,
                "location_type": 1,
                "longitude": -71.029583,
                "municipality": "Quincy",
                "name": "North Quincy",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-nqncy",
            "links": {
                "self": "/stops/place-nqncy"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-nqncy"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "90 Woodbine St, Quincy, MA 02171",
                "at_street": None,
                "description": None,
                "latitude": 42.266514,
                "location_type": 1,
                "longitude": -71.020337,
                "municipality": "Quincy",
                "name": "Wollaston",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-wlsta",
            "links": {
                "self": "/stops/place-wlsta"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-wlsta"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "175 Thomas E Burgin Pkwy, Quincy, MA 02169",
                "at_street": None,
                "description": None,
                "latitude": 42.251809,
                "location_type": 1,
                "longitude": -71.005409,
                "municipality": "Quincy",
                "name": "Quincy Center",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-qnctr",
            "links": {
                "self": "/stops/place-qnctr"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-qnctr"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": {
                        "id": "CR-zone-1",
                        "type": "zone"
                    }
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "Burgin Pkwy and Centre St, Quincy, MA 02169",
                "at_street": None,
                "description": None,
                "latitude": 42.233391,
                "location_type": 1,
                "longitude": -71.007153,
                "municipality": "Quincy",
                "name": "Quincy Adams",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-qamnl",
            "links": {
                "self": "/stops/place-qamnl"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-qamnl"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": None
                }
            },
            "type": "stop"
        },
        {
            "attributes": {
                "address": "197 Ivory St, Braintree, MA 02184",
                "at_street": None,
                "description": None,
                "latitude": 42.207854,
                "location_type": 1,
                "longitude": -71.001138,
                "municipality": "Braintree",
                "name": "Braintree",
                "on_street": None,
                "platform_code": None,
                "platform_name": None,
                "vehicle_type": None,
                "wheelchair_boarding": 1
            },
            "id": "place-brntn",
            "links": {
                "self": "/stops/place-brntn"
            },
            "relationships": {
                "facilities": {
                    "links": {
                        "related": "/facilities/?filter[stop]=place-brntn"
                    }
                },
                "parent_station": {
                    "data": None
                },
                "zone": {
                    "data": {
                        "id": "CR-zone-2",
                        "type": "zone"
                    }
                }
            },
            "type": "stop"
        }
    ],
    "jsonapi": {
        "version": "1.0"
    }
}


class TestMBTARouteService(unittest.TestCase):
    def setUp(self) -> None:
        self.route_service = route_service.MBTARouteService()
        self.route_path = f"{self.route_service.base_url}{self.route_service.route_path}"
        self.stop_path = f"{self.route_service.base_url}{self.route_service.stop_path}"

    def test_routes_no_routes(self):
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=ROUTE_RESPONSE)
            self.assertEqual(0, len(self.route_service.routes), "Too many routes")

    def test_routes_one_route(self):
        one_route_response = copy.deepcopy(ROUTE_RESPONSE)
        one_route_response["data"].append(RED_ROUTE)
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=one_route_response)
            response.add(responses.GET, self.stop_path, json=RED_STOP_RESPONSE)
            expected_routes = len(one_route_response["data"])
            actual_routes = len(self.route_service.routes)
            self.assertEqual(expected_routes, actual_routes, f"Expected {expected_routes} routes, but found {actual_routes} routes")

    def test_routes_multiple_routes(self):
        multi_route_response = copy.deepcopy(ROUTE_RESPONSE)

        multi_route_response["data"].append(RED_ROUTE)
        multi_route_response["data"].append(GREEN_B_ROUTE)
        multi_route_response["data"].append(MATTAPAN_ROUTE)
        stop_ids = set(s["id"] for s in RED_STOP_RESPONSE["data"] + GREEN_B_STOP_RESPONSE["data"] + MATTAPAN_STOP_RESPONSE["data"])

        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=multi_route_response)
            response.add(
                responses.GET, self.stop_path,
                match=[responses.matchers.query_param_matcher({"filter[route]": RED_ROUTE["id"]})],
                json=RED_STOP_RESPONSE
            )
            response.add(
                responses.GET, self.stop_path,
                match=[responses.matchers.query_param_matcher({"filter[route]": GREEN_B_ROUTE["id"]})],
                json=GREEN_B_STOP_RESPONSE
            )
            response.add(
                responses.GET, self.stop_path,
                match=[responses.matchers.query_param_matcher({"filter[route]": MATTAPAN_ROUTE["id"]})],
                json=MATTAPAN_STOP_RESPONSE
            )
            self.assertEqual(len(multi_route_response["data"]), len(self.route_service.routes), "Too many routes")
            self.assertEqual(len(stop_ids), len(self.route_service.stops), f"Expected {len(stop_ids)} stops, but found {len(self.route_service.stops)} stops")

    def test_route_exists(self):
        one_route_response = copy.deepcopy(ROUTE_RESPONSE)

        one_route_response["data"].append(RED_ROUTE)
        expected_route = route_service.MBTARoute(RED_ROUTE)
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=one_route_response)
            response.add(responses.GET, self.stop_path, json=RED_STOP_RESPONSE)
            self.assertEqual(expected_route, self.route_service.route(expected_route.id), "Route ID does not index the expected route")
            self.assertEqual(expected_route, self.route_service.route(str(expected_route)), "Route string does not index the expected route")

    def test_route_not_exists(self):
        unexpected_route = route_service.MBTARoute(RED_ROUTE)
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=ROUTE_RESPONSE)
            self.assertIsNone(self.route_service.route(unexpected_route.id), f"Route ID, {unexpected_route.id}, indexed an unexpected route")
            self.assertIsNone(self.route_service.route(str(unexpected_route)), f"Route string, {unexpected_route}, indexed an unexpected route")

    def test_stops_no_stops(self):
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=ROUTE_RESPONSE)
            self.assertEqual(0, len(self.route_service.stops), "Unexpected stops")

    def test_stops_one_stop(self):
        one_route_response = copy.deepcopy(ROUTE_RESPONSE)
        one_route_response["data"].append(RED_ROUTE)
        one_stop_response = {
            "data": [RED_STOP_RESPONSE["data"][0]],
            "jsonapi": {
                "version": "1.0"
            }
        }
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=one_route_response)
            response.add(responses.GET, self.stop_path, json=one_stop_response)
            stop_count = len(self.route_service.stops)
            self.assertEqual(1, stop_count, f"Expected 1 stop, but found {stop_count} stops")

    def test_stops_multiple_stops(self):
        multiple_stop_response = copy.deepcopy(ROUTE_RESPONSE)

        multiple_stop_response["data"].append(RED_ROUTE)
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=multiple_stop_response)
            response.add(responses.GET, self.stop_path, json=RED_STOP_RESPONSE)
            expected_stop_count = len(RED_STOP_RESPONSE["data"])
            stop_count = len(self.route_service.stops)
            self.assertEqual(expected_stop_count, stop_count, f"Expected {expected_stop_count} stop, but found {stop_count} stops")

    def test_stop_exists(self):
        multiple_stop_response = copy.deepcopy(ROUTE_RESPONSE)

        multiple_stop_response["data"].append(RED_ROUTE)
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=multiple_stop_response)
            response.add(responses.GET, self.stop_path, json=RED_STOP_RESPONSE)
            expected_stop = route_service.MBTAStop(RED_STOP_RESPONSE["data"][0])
            self.assertEqual(expected_stop, self.route_service.stop(expected_stop.id), f"Stop ID, {expected_stop.id}, does not index the expected stop")
            self.assertEqual(expected_stop, self.route_service.stop(str(expected_stop)), f"Stop string, {expected_stop}, does not index the expected stop")

    def test_stop_not_exists(self):
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=ROUTE_RESPONSE)
            unexpected_stop = route_service.MBTAStop(RED_STOP_RESPONSE["data"][0])
            self.assertIsNone(self.route_service.stop(unexpected_stop.id), f"Stop ID, {unexpected_stop.id}, indexed an unexpected stop")
            self.assertIsNone(self.route_service.stop(str(unexpected_stop)), f"Stop string, {unexpected_stop}, indexed an unexpected stop")

    def test_trip_exists(self):
        trip_response = copy.deepcopy(ROUTE_RESPONSE)

        trip_response["data"].append(RED_ROUTE)
        trip_response["data"].append(GREEN_B_ROUTE)
        trip_response["data"].append(MATTAPAN_ROUTE)
        red_route = route_service.MBTARoute(RED_ROUTE)
        green_b_route = route_service.MBTARoute(GREEN_B_ROUTE)
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=trip_response)
            response.add(
                responses.GET, self.stop_path,
                match=[responses.matchers.query_param_matcher({"filter[route]": RED_ROUTE["id"]})],
                json=RED_STOP_RESPONSE
            )
            response.add(
                responses.GET, self.stop_path,
                match=[responses.matchers.query_param_matcher({"filter[route]": GREEN_B_ROUTE["id"]})],
                json=GREEN_B_STOP_RESPONSE
            )
            response.add(
                responses.GET, self.stop_path,
                match=[responses.matchers.query_param_matcher({"filter[route]": MATTAPAN_ROUTE["id"]})],
                json=MATTAPAN_STOP_RESPONSE
            )
            starting_stop = self.route_service.stop("Ashmont")
            destination_stop = self.route_service.stop("Arlington")
            trip = self.route_service.trip(starting_stop, destination_stop)
            self.assertListEqual([red_route, green_b_route], trip, "Expected trip was not produced!")

    def test_trip_not_exists(self):
        trip_response = copy.deepcopy(ROUTE_RESPONSE)

        trip_response["data"].append(MATTAPAN_ROUTE)
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=trip_response)
            response.add(
                responses.GET, self.stop_path,
                match=[responses.matchers.query_param_matcher({"filter[route]": MATTAPAN_ROUTE["id"]})],
                json=MATTAPAN_STOP_RESPONSE
            )
            starting_stop = self.route_service.stop("Ashmont")
            destination_stop = self.route_service.stop("Arlington")
            trip = self.route_service.trip(starting_stop, destination_stop)
            self.assertListEqual([], trip, "Trip exists")

    def test_routes_status_400(self):
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, status=400)
            self.assertRaises(route_service.RouteServiceHttpException, self.route_service.route, "X")

    def test_routes_status_403(self):
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, status=403)
            self.assertRaises(route_service.RouteServiceHttpException, self.route_service.route, "X")

    def test_routes_status_429(self):
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, status=429)
            self.assertRaises(route_service.RouteServiceHttpException, self.route_service.route, "X")

    def test_routes_malformed_json(self):
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json={})
            self.assertRaises(route_service.RouteServiceJsonException, self.route_service.route, "X")

    def test_stops_status_400(self):
        stop_response = copy.deepcopy(ROUTE_RESPONSE)
        stop_response["data"].append(MATTAPAN_ROUTE)
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=stop_response)
            response.add(responses.GET, self.stop_path, status=400)
            self.assertRaises(route_service.RouteServiceHttpException, self.route_service.route, "X")

    def test_stops_status_403(self):
        stop_response = copy.deepcopy(ROUTE_RESPONSE)
        stop_response["data"].append(MATTAPAN_ROUTE)
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=stop_response)
            response.add(responses.GET, self.stop_path, status=403)
            self.assertRaises(route_service.RouteServiceHttpException, self.route_service.route, "X")

    def test_stops_status_429(self):
        stop_response = copy.deepcopy(ROUTE_RESPONSE)
        stop_response["data"].append(MATTAPAN_ROUTE)
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=stop_response)
            response.add(responses.GET, self.stop_path, status=429)
            self.assertRaises(route_service.RouteServiceHttpException, self.route_service.route, "X")

    def test_stops_malformed_json(self):
        stop_response = copy.deepcopy(ROUTE_RESPONSE)
        stop_response["data"].append(MATTAPAN_ROUTE)
        with responses.RequestsMock() as response:
            response.add(responses.GET, self.route_path, json=stop_response)
            response.add(responses.GET, self.stop_path, json={})
            self.assertRaises(route_service.RouteServiceJsonException, self.route_service.route, "X")

