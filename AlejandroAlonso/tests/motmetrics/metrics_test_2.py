import motmetrics as mm
# List all default metrics
mh = mm.metrics.create()
print(mh.list_metrics_markdown())