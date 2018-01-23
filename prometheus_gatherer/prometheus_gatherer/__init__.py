from prometheus_client.parser import text_string_to_metric_families
import requests

# Scrape metrics
metrics = requests.get('http://127.0.0.1:5000/metrics')
if metrics:
    metrics = metrics.text
metrics = text_string_to_metric_families(metrics)
# Code copied from prometheus_client multiprocessing.py

for metric in metrics:
    samples = {}
    buckets = {}
    print(metric.samples)
    for name, labels, value in metric.samples:
        if metric.type == 'gauge':
            pass
            #print(labels)
            #samples[(name, labels)] = value
        elif metric.type == 'histogram':
            bucket = [float(l[1]) for l in labels if l[0] == 'le']
            if bucket:
                # _bucket
                without_le = tuple([l for l in labels if l[0] != 'le'])
                buckets.setdefault(without_le, {})
                buckets[without_le].setdefault(bucket[0], 0.0)
                buckets[without_le][bucket[0]] += value
            else:
                # _sum/_count
                samples.setdefault((name, labels), 0.0)
                samples[(name, labels)] += value
        else:
            # Counter and Summary.
            samples.setdefault((name, labels), 0.0)
            samples[(name, labels)] += value


    # Accumulate bucket values.
    if metric.type == 'histogram':
        for labels, values in buckets.items():
            acc = 0.0
            for bucket, value in sorted(values.items()):
                acc += value
                samples[(metric.name + '_bucket', labels + (('le', core._floatToGoString(bucket)), ))] = acc
            samples[(metric.name + '_count', labels)] = acc

    # Convert to correct sample format.
    metric.samples = [(name, dict(labels), value) for (name, labels), value in samples.items()]
print(metrics.values())
