import logging
from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional, Tuple

import pygtfs

from pyraptor.model import Route, Transfer, StopTime


class Timetable(object):
    def __init__(self, schedule: pygtfs.Schedule) -> None:
        """
        Construct the in-memory data structures for timetable traversal
        and querying.
        """
        self.logger = logging.getLogger(__name__)
        self.schedule = schedule
        self.stop_ids = self._build_stop_ids()
        self.stops_dict = self._build_stops_dict()

        # For now this is only using GTFS tranfers.txt, but maybe a simple
        # walk + transit router can be made by dynamically adding footpaths
        # from the query origin/destination to stops within some radius.
        self.transfers = self._build_transfers()

        self._build_routes()

    def earliest_trip(
        self,
        route: Route,
        stop_seq: int,
        min_departure_time: int
    ) -> Optional[int]:
        """
        Return the earliest trip leaving from the input stop, if found.
        """
        trip_idx = route.stop_times_idx
        for _ in range(route.num_trips):
            stop_time = self.stop_times[trip_idx + stop_seq]
            if stop_time.departure_time >= min_departure_time:
                return trip_idx

            trip_idx += route.num_stops

        return None

    def _build_stop_ids(self) -> List[str]:
        return [s.stop_id for s in self.schedule.stops]

    def _build_stops_dict(self) -> Dict[str, pygtfs.gtfs_entities.Stop]:
        return {s.stop_id: s for s in self.schedule.stops}

    def _build_transfers(self) -> List[Transfer]:
        return [
            Transfer(
                from_stop_id=t.from_stop_id,
                to_stop_id=t.to_stop_id,
                transfer_time_mins=t.min_transfer_time or 0,
            ) for t in self.schedule.transfers
        ]

    def _build_routes(self):
        """
        Construct the "Routes"/"StopTimes"/"RouteStops" arrays from Appx A.

        RAPTOR expects a "route" to only contain trips that all have the same
        stop sequence. This means we cannot reuse GTFS route objects, because
        they do not obey this constraint by grouping both directions as a
        single route AND by grouping trips with different stop sequences as
        part of same route.
        """
        trips = defaultdict(lambda: [])  # type: DefaultDict[str, List[StopTime]]
        for stop_time in self.schedule.stop_times:
            trips[stop_time.trip_id].append(
                StopTime(
                    stop_id=stop_time.stop_id,
                    trip_id=stop_time.trip_id,
                    arrival_time=stop_time.arrival_time.seconds,
                    departure_time=stop_time.departure_time.seconds
                )
            )

        trip_groups = defaultdict(lambda: [])  # type: DefaultDict[str, List[Tuple[str, List[StopTime]]]]
        for trip_id, stop_times in trips.items():
            stop_sequence = ''.join(
                [stop_time.stop_id for stop_time in stop_times]
            )
            trip_groups[stop_sequence].append((trip_id, stop_times))

        self.stop_times = []  # type: List[StopTime]
        self.route_stops = []  # type: List[str]
        self.routes = []  # type: List[Route]

        for trip_group in trip_groups.values():
            # All the trip_ids should refer to the same GTFS route
            first_trip_id = trip_group[0][0]
            # All stop_times have the same stop sequence
            first_stop_times = trip_group[0][1]

            self.routes.append(
                Route(
                    gtfs_route_id=self.schedule.trips_by_id(first_trip_id)[0].route_id,
                    num_trips=len(trip_group),
                    num_stops=len(first_stop_times),
                    route_stop_idx=len(self.route_stops),
                    stop_times_idx=len(self.stop_times),
                )
            )

            for stop_time in first_stop_times:
                self.route_stops.append(stop_time.stop_id)

            all_stop_times = [trip[1] for trip in trip_group]
            sorted_stop_times = sorted(
                all_stop_times, key=lambda x: x[0].arrival_time
            )
            self.stop_times += [
                s for stop_times in sorted_stop_times for s in stop_times
            ]
