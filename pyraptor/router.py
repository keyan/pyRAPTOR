import datetime
import sys

import pygtfs

from pyraptor.timetable import Timetable

# Supposedly bounding is not required but haven't figured out how to remove it yet
MAX_TRIPS = 5


class Router(object):
    def __init__(self):
        pass

    def find_route(
        self,
        origin_stop_id: str,
        dest_stop_id: str,
        timetable: Timetable,
        departure_time: int = None,
    ):
        if departure_time is None:
            departure_time = Router._get_current_time_seconds()

        # Map each stop_id to a list of earliest arrival times where index i in the list
        # corresponds to the earliest arrival known arrival time with up to i trips
        labels = {stop_id: [float('inf')] for stop_id in timetable.stop_ids}

        # Earliest arrival at the origin requires no trips
        labels[origin_stop_id][0] = departure_time

        # Determine the earliest arrival to every stop using up to k trips
        for k in range(1, MAX_TRIPS):
            # First stage - set upper bound for earliest arrival as best for previous round
            # This can be removed with 'local pruning'
            [labels[stop_id].append(labels[stop_id][-1]) for stop_id in labels.keys()]

            for idx, route in enumerate(timetable.routes):
                curr_trip_idx = None  # type: Optional[int]
                departure = float('inf')

                for stop_seq in range(route.num_stops):
                    stop_id = timetable.route_stops[route.route_stop_idx + stop_seq]

                    # Must be modified when adding 'local pruning'
                    if curr_trip_idx is not None:
                        stop_time = timetable.stop_times[curr_trip_idx + stop_seq]
                        assert stop_id == stop_time.stop_id
                        labels[stop_id][k] = stop_time.arrival_time
                        departure = stop_time.departure_time

                    # Check if there an earlier trip to this stop
                    if labels[stop_id][k - 1] <= departure:
                        min_departure_time = labels[stop_id][k - 1]
                        curr_trip_idx = timetable.earliest_trip(route, stop_seq, min_departure_time)

            # for transfer in timetable.transfers:
            #     labels[

        return labels[dest_stop_id]

    @staticmethod
    def _get_current_time_seconds():
        now = datetime.datetime.now()
        return datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second).seconds
