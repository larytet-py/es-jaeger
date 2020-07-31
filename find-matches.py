import argparse
import sys
import json
import re

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
    if len_spans > 18:
        hit = hits[trace_id][0]
        hit_source = hit["_source"]
        hit_tags = hit_source["tags"]
        global_tx_id = "?"
        for hit_tag in hit_tags:
            if hit_tag["key"] == "http.path":
                hit_tag_value = hit_tag["value"]
                global_tx_id = re.match("/tm/v2/transaction/(.+)", hit_tag_value).group(1)
        print(f"https://ghosts.awseu.apollo-prod.cyren.cloud/jaeger/trace/{trace_id}   {global_tx_id}")
    max_trace = max(max_trace, len_spans)
    min_trace = min(min_trace, len_spans)
    histogram[len_spans] = histogram.get(len_spans, 0) + 1

print(sorted(histogram.items()))
