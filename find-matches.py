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
    #print(len(hits[trace_id]))

#print(hits[trace_id])
min_trace = len(hits[trace_id])
max_trace = min_trace
histogram = {}
for trace_id in hits:
    len_spans = len(hits[trace_id])
    max_trace = max(max_trace, len_spans)
    min_trace = min(min_trace, len_spans)
    histogram[len_spans] = histogram.get(len_spans, 0) + 1

print(sorted(histogram.items()))
