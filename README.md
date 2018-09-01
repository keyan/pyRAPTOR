Implementation of Round bAsed Public Transit Optimized Router (RAPTOR): https://www.microsoft.com/en-us/research/publication/round-based-public-transit-routing/

### Usage

```
python3 pyraptor/db_loader.py static/bart.gtfs.zip

python3 pyraptor/main.py --origin <STOP_ID> --dest <STOP_ID>
```

### Optimizations

- local pruning
- cleanup db loading/settings
- add flask server

### Known issues

- Timezone not considered, so queries without explicit departure time assume departure time is now for local timezone, but do not convert to transit agency timezone

