import argparse
import sys

import pygtfs

from pyraptor.settings import DB_FILENAME
from pyraptor.router import Router
from pyraptor.timetable import Timetable


def parse_cmd_line(args):
    parser = argparse.ArgumentParser(description='TODO')

    parser.add_argument(
        '--orgin',
        action='store',
        dest='origin_stop_id',
        default='M06N',
        help='TODO',
    )
    parser.add_argument(
        '--dest',
        action='store',
        dest='destination_stop_id',
        default='103',
        help='TODO',
    )

    return parser.parse_args(args)


def main(origin_stop_id, destination_stop_id):
    schedule = pygtfs.Schedule(DB_FILENAME)
    timetable = Timetable(schedule)

    router = Router()

    result = router.route(
        origin_stop_id=parsed.origin_stop_id,
        destination_stop_id=parsed.destination_stop_id,
        timetable=timetable,
    )

    return result


if __name__ == '__main__':
    parsed = parse_cmd_line(sys.argv[1:])

    result = main(
        origin_stop_id=parsed.origin_stop_id,
        destination_stop_id=parsed.destination_stop_id,
    )

    print(result)
