import sys

import pygtfs

import Timetable

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

            for route in timetable.routes.values():
                curr_trip_id = None  # type: Optional[str]
                best_departure = float('inf')

                for stop_id in route.route_stop_ids:
                    # Must be modified when adding 'local pruning'
                    if (
                        curr_trip_id is not None and
                        curr_trip_id[stop_id].arrival_time < labels[stop_id][k - 1]
                    ):
                        labels[stop_id][k] = curr_trip[stop_id].arrival_time

                    if labels[stop_id][k - 1] <= best_departure:
                        min_departure_time = labels[stop_id][k - 1]
                        curr_trip = timetable.earliest_trip(route, stop_id, min_departure_time)

    @staticmethod
    def _get_current_time_seconds():
        now = datetime.datetime.now()
        return datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second).seconds
