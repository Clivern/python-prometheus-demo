## Replacement for the prometheus Python client multiprocess mode

```
application <- prometheus_gatherer <- prometheus server
```

`prometheus_gatherer` runs as a sidecar service along with your
Python application

### Expectations from Application

HTTP applications: expose a `/metrics` HTTP endpoint
non-HTTP services: expose a `/metrics` HTTP endpoint

### Desired features

- Do the same job as multiprocessing mode
- Not use any filesystem files for bookkeeping
- Don't worry about workers dying

### Implementation

- (Similar to statsd exporter; but the input is prometheus metrics)
- Scrape target
- Parse metrics
- (See multiprocess mode to borrow ideas)

### Advantages over statsd exporter?

- Able to use native prometheus exporting with multi process
  Python applications
