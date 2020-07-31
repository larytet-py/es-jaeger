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
    hits[trace_id] = hits.get(trace_id, []).append(hit)

min = len(hits[trace_id])
max = min
for spans in hits:
    max = max(max, len(spans))
    min = min(min, len(spans))

print(max, min)
