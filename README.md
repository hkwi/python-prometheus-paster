
Configuration example

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
