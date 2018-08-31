from typing import List


class StopTime(object):
    def __init__(
        self,
        stop_id: str,
        arrival_time: int,
        departure_time: int,
    ) -> None:
        self.stop_id = stop_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time


class Transfer(object):
    def __init__(
        self,
        from_stop_id: str,
        to_stop_id: str,
        transfer_time_mins: int,
    ) -> None:
        self.from_stop_id = from_stop_id
        self.to_stop_id = to_stop_id
        self.transfer_time_mins = transfer_time_mins


class Route(object):
    def __init__(
        self,
        gtfs_route_id: str,
        num_trips: int,
        num_stops: int,
        route_stop_idx: int,
        stop_times_idx: int,
    ) -> None:
        # This allows us to retrieve the real GTFS route for post-routing
        # presentation to the user
        self.gtfs_route_id = gtfs_route_id

        self.num_trips = num_trips
        self.num_stops = num_stops
        self.route_stop_idx = route_stop_idx
        self.stop_times_idx = stop_times_idx
