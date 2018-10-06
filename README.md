Implementation of Round bAsed Public Transit Optimized Router (RAPTOR): https://www.microsoft.com/en-us/research/publication/round-based-public-transit-routing/

### Usage

Currently hardcoded to use the BART GTFS feed stored as a sqllite db:  `db/gtfs_db`.

1. Install dependencies
    ```
    pip3 install requirements.txt
    ```
1. Load GTFS data into local SQLite DB
    ```
    python3 ./pyraptor/db_loader.py <gtfs_file.zip>
    ```
1. Run server
    ```
    FLASK_DEBUG=1 FLASK_APP=pyraptor flask run
    ```
1. Issue requests using GTFS specified stop ids. For BART these are the first column here: https://transitfeeds-data.s3-us-west-1.amazonaws.com/public/feeds/bart/58/20180920/original/stops.txt
    ```
    curl "http://127.0.0.1:5000/route?origin_stop_id=12TH&dest_stop_id=19TH" | jq .

    [
    [
        "9:38:53 -- Embark from: 12th St. Oakland City Center",
        "Take the Richmond - Daly City/Millbrae Subway towards Richmond",
        "9:49:00 -- Disembark at: 19th St. Oakland"
    ]
    ]
    ```

### Optimizations

- add transfers
- local pruning
- cleanup db loading/settings

### Known issues

- Timezone not considered, so queries without explicit departure time assume departure time is now for local timezone, but do not convert to transit agency timezone
- Day of week not considered, to fix this update `stop_times` building in `timetable.py` to cross-reference information in `trips.txt` to only add stop times relevant for the current day
