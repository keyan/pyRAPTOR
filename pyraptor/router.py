import copy
import datetime
import sys
from typing import Dict, List

import pygtfs

from pyraptor.constants import GtfsRouteType
from pyraptor.settings import DB_FILENAME
from pyraptor.timetable import Timetable

# Supposedly bounding is not required but haven't figured out how to remove it yet
MAX_TRIPS = 5


class Label(object):
    def __init__(
        self,
        stop_id: str,
        arrival_time: float = float('inf'),
        boarded_stop_id: str = None,
        route_idx: int = None,
        trip_id: str = None,
    ):
        self.stop_id = stop_id
        self.arrival_time = arrival_time
        self.boarded_stop_id = boarded_stop_id
        self.route_idx = route_idx
        self.trip_id = trip_id


class Router(object):
    def __init__(self):
        self.schedule = pygtfs.Schedule(DB_FILENAME)
        self.timetable = Timetable(self.schedule)

    def find_routes(
        self,
        origin_stop_id: str,
        dest_stop_id: str,
        departure_time: int = None,
    ):
        if departure_time is None:
            departure_time = Router._get_current_time_seconds()

        labels = self._compute_labels(origin_stop_id, dest_stop_id, departure_time)

        return self._build_itineraries(origin_stop_id, dest_stop_id, departure_time, labels)
        # import ipdb;ipdb.set_trace()
        # return [s.__dict__ for s in labels[dest_stop_id]]

    def _build_itineraries(
        self,
        origin_stop_id: str,
        dest_stop_id: str,
        departure_time: int,
        labels: Dict[str, List[Label]],
    ) -> List[List[str]]:
        """
        """
        results = []
        for k in range(1, MAX_TRIPS):
            itinerary = []
            curr_stop = labels[dest_stop_id][k]
            if labels[dest_stop_id][k - 0].arrival_time < curr_stop.arrival_time:
                break

            while curr_stop.boarded_stop_id != None and curr_stop.arrival_time != float('inf'):
                print(curr_stop.__dict__)

                disembark_time = datetime.timedelta(seconds=curr_stop.arrival_time)
                itinerary.append(f'{disembark_time} -- Disembark at: {router.timetable.stops_dict[curr_stop.stop_id].stop_name}')

                headsign = self.schedule.trips_by_id(curr_stop.trip_id)[0].trip_headsign
                timetable_route = router.timetable.routes[curr_stop.route_idx]
                route = self.schedule.routes_by_id(timetable_route.gtfs_route_id)[0]
                gtfs_route_type = GtfsRouteType(route.route_type).name
                itinerary.append(f'Take the "{route.route_long_name}" {gtfs_route_type} towards {headsign}')
                curr_stop = labels[curr_stop.boarded_stop_id][k]

            if curr_stop.arrival_time == float('inf'):
                continue

            origin_stop = self.schedule.stops_by_id(curr_stop.stop_id)[0]
            embark_time = datetime.timedelta(seconds=departure_time)
            itinerary.append(f'{embark_time} -- Embark from: {router.timetable.stops_dict[curr_stop.stop_id].stop_name}')

            itinerary.reverse()
            results.append(itinerary)

        return results if len(results) > 0 else 'No routes found'

    def _compute_labels(
        self,
        origin_stop_id: str,
        dest_stop_id: str,
        departure_time: int,
    ) -> Dict[str, List[Label]]:
        """
        """
        # Map each stop_id to a list of earliest arrival times where index i in the list
        # corresponds to the earliest arrival known arrival time with up to i trips
        labels = {stop_id: [Label(stop_id=stop_id)] for stop_id in self.timetable.stop_ids}

        # Earliest arrival at the origin requires no trips
        labels[origin_stop_id][0].arrival_time = departure_time

        # Determine the earliest arrival to every stop using up to k trips
        for k in range(1, MAX_TRIPS):
            # First stage - set upper bound for earliest arrival as best for previous round
            # This can be removed with 'local pruning'
            [labels[stop_id].append(copy.deepcopy(labels[stop_id][-1])) for stop_id in labels.keys()]

            for idx, route in enumerate(self.timetable.routes):
                curr_trip_idx = None  # type: Optional[int]
                boarded_stop_id = None  # type: Optional[int]
                departure = float('inf')

                for stop_seq in range(route.num_stops):
                    stop_id = self.timetable.route_stops[route.route_stop_idx + stop_seq]

                    # Must be modified when adding 'local pruning'
                    if curr_trip_idx is not None:
                        stop_time = self.timetable.stop_times[curr_trip_idx + stop_seq]
                        assert stop_id == stop_time.stop_id
                        labels[stop_id][k] = Label(
                            stop_id=stop_id,
                            arrival_time=stop_time.arrival_time,
                            boarded_stop_id=boarded_stop_id,
                            trip_id=stop_time.trip_id,
                            route_idx=idx,
                        )
                        departure = stop_time.departure_time

                    # Check if there an earlier trip to this stop
                    if labels[stop_id][k - 1].arrival_time <= departure:
                        min_departure_time = labels[stop_id][k - 1].arrival_time
                        curr_trip_idx = self.timetable.earliest_trip(route, stop_seq, min_departure_time)
                        boarded_stop_id = stop_id

            # TODO - process transfers

        return labels

    @staticmethod
    def _get_current_time_seconds():
        now = datetime.datetime.now()
        return datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second).seconds


router = Router()
