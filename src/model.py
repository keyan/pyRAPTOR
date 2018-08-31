from typing import List


class StopTime(object):
    def __init__(self, stop_id: str, arrival_time: int, departure_time: int):
        self.stop_id = stop_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time


class Transfer(object):
    def __init__(self, from_stop_id: str, to_stop_id: str, transfer_time_mins: int):
        self.from_stop_id = from_stop_id
        self.to_stop_id = to_stop_id
        self.transfer_time_mins = transfer_time_mins


class Route(object):
    def __init__(
        self,
        route_id: str,
        route_stops_ids: List[str],
        stop_times: List[StopTime],
    ):
        self.route_id = route_id
        self.route_stops = route_stops

        # Using the idea presented in Appx A, this list is ordered such that
        # index 0 represents the earliest StopTime at the route's initial stop
        # while index len(route_stop_ids) is the StopTime for second
        # earliest trip departing from the initial stop. This allows for
        # constant time earliest_trip calculation.
        self.stop_times = stop_times
