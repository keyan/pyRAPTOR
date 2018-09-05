Implementation of Round bAsed Public Transit Optimized Router (RAPTOR): https://www.microsoft.com/en-us/research/publication/round-based-public-transit-routing/

### Usage

Currently hardcoded to use the BART GTFS feed stored as a sqllite db:  `db/gtfs_db`.

```
pip3 install requirements.txt

FLASK_DEBUG=1 FLASK_APP=pyraptor flask run

curl "http://127.0.0.1:5000/route?origin_stop_id=12TH&dest_stop_id=24TH"
```

### Optimizations

- add transfers
- local pruning
- cleanup db loading/settings

### Known issues

- Timezone not considered, so queries without explicit departure time assume departure time is now for local timezone, but do not convert to transit agency timezone

