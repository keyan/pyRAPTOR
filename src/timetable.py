import pygtfs

import Route, Stop, Trip


class Timetable(object):
    def __init__(self, schedule: pygtfs.Schedule) -> None:
        """
        Construct the in-memory data structures for timetable traversal
        and querying.

        Note that none of the adjaceny structure optimizations from
        Appx A are mirrored. Only the ordering of the StopTimes list is
        """
        self.schedule = schedule

        self.stop_ids = self._build_stop_ids()
        self.transfers = self._build_transfers()

        self._build_trips_and_routes()

    def earliest_trip(
        self,
        route: Route,
        stop_id: str,
        min_departure_time: int
    ) -> Optional[str]:
        """
        Return the earliest trip leaving from the input stop, if found.
        """
        return None

    def _build_stop_ids(self) -> List[str]:
        return [s.stop_id for s in self.schedule.stops]

    def _build_transfers(self):
        return [
            Transfer(
                from_stop_id=t.from_stop_id,
                to_stop_id=t.to_stop_id,
                transfer_time_mins=t.min_transfer_time or 0,
            ) for t in self.schedule.transfers
        ]

    def _build_trips_and_routes(self):
        self.routes = {
            r.route_id: Route(route_id=r.route_id, route_stop_ids=[], stop_times=[])
            for r in self.schedule.routes
        }

        curr_trip_id = None
        curr_route_id = None
        curr_stop_times = []
        for stop_time in self.schedule.stop_times:
            if curr_trip_id is None or stop_time.trip_id != curr_trip_id:
                curr_trip_id = stop_time.trip_id
                curr_route_id
