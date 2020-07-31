import argparse
import sys
import json


filename = sys.argv[1]
with open(filename, "r") as f:
    data = json.load(f)

hits = {}
for hit in data["hits"]["hits"]:
    print(hit)
    hit_source = hit["_source"]
    trace_id = hit_source["traceID"]
    traces[trace_id] = traces.get(trace_id, []).append(hit)

min = len(traces[trace_id])
max = min
for spans in traces:
    max = max(max, len(spans))
    min = min(min, len(spans))

print(max, min)