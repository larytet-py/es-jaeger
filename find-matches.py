import argparse
import sys
import json


filename = sys.argv[1]
with open(filename, "r") as f:
    data = json.load(f)

hits = {}
for hit in data["hits"]["hits"]:
    hit_source = hit["_source"]
    trace_id = hit_source["traceID"]
    spans = hits.get(trace_id, [])
    spans.append(hit)
    hits[trace_id] = spans

min_trace = len(hits[trace_id])
max_trace = min_trace
for spans in hits:
    max_trace = max(max_trace, len(spans))
    min_trace = min(min_trace, len(spans))

print(max_trace, min_trace)
