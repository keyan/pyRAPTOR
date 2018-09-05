from enum import Enum


class GtfsRouteType(Enum):
    Unknown = -1
    Tram = 0
    Subway = 1
    Rail = 2
    Bus = 3
    Ferry = 4
    Cable_car = 5
    Gondola = 6
    Funicular = 7
