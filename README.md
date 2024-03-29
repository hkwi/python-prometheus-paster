This is a glue between [prometheus_client](https://github.com/prometheus/client_python) and [pastedeploy](https://docs.pylonsproject.org/projects/pastedeploy/en/latest/).

# Quick start

configuration example

```
[composite:main]
use = egg:Paste#urlmap
/metrics = prom
/ = papp

[pipeline:papp]
pipeline = perf app

[app:app]
use = egg:someapp

[filter:perf]
use = egg:prometheus_paster#filter
name = someapp_call

[app:prom]
use = egg:prometheus_paster
```

## Prometheus exporter endpoint Configuration

You can expose the endpoint with `egg:prometheus_paster` wsgi application.

```
[app:main]
use = egg:prometheus_paster
```

## Collector filter Configuration

- latency : metric name for wsgi processing time (default `response_latency_seconds`)
- length : metric name for wsgi response length (default `response_length_bytes`)
- path_regex : if request path does not match this regex, then it will be ignored. (default `.*`)
- disable_latency: if set to true, then latency metrics will not be collected.
- disable_length: if set to true, then length metrics will not be collected.


## Multiple metrics (1)

If you want to collect two different application on the same wsgi container, 
then you can put different filters.

```
[composite:main]
use = egg:Paste#urlmap
/metrics = prom
/app1 = app1
/app2 = app2

[app:app1]
use = egg:app1
filter-with = app1_perf

[filter:app1_perf]
use = egg:prometheus_paster#filter
latency = app1_latency
length = app1_length

[app:app2]
use = egg:app2
filter-with = app2_perf

[filter:app2_perf]
use = egg:prometheus_paster#filter
latency = app2_latency
length = app2_length

[app:prom]
use = egg:prometheus_paster
```


## Multiple metrics (2)

Another option is stacking filters.

```
[composite:main]
use = egg:Paste#urlmap
/metrics = prom
/app = app1_pipe

[pipeline:app1_pipe]
pipeline = path1_perf path2_perf app1

[app:app1]
use = egg:app1

[filter:path1_perf]
use = egg:prometheus_paster#filter
latency = path1_latency
length = path1_length
path_regex = /path1/.*

[filter:path2_perf]
use = egg:prometheus_paster#filter
latency = path2_latency
length = path2_length
path_regex = /path2/.*

[app:prom]
use = egg:prometheus_paster
```
