import argparse
import sys
import json
import re


hits = {}
processed_filenames = {}
for filename in sys.argv[1:]:
    if filename in processed_filenames:
        print(f"I have seen {filename} already")
        continue
    with open(filename, "r") as f:
        data = json.load(f)

    for hit in data["hits"]["hits"]:
        hit_source = hit["_source"]
        trace_id = hit_source["traceID"]
        spans = hits.get(trace_id, [])
        spans.append(hit)
        hits[trace_id] = spans
        #print(len(hits[trace_id]))
    processed_filenames[filename] = True

print(f"Processed {len(processed_filenames)} files")

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
        print(f"{trace_id}   {global_tx_id}")

    max_trace = max(max_trace, len_spans)
    min_trace = min(min_trace, len_spans)
    histogram[len_spans] = histogram.get(len_spans, 0) + 1

sorted_items = sorted(histogram.items())

for i in sorted_items:
    print("({:>2},{:>3}) ".format(i[0], i[1]), end="")
print()

acc = 0
subtotals = []
for i in sorted_items:
    acc += i[1] 
    subtotals.append(acc)
    print("{:>8} ".format(acc), end="")
print()

for subtotal in subtotals:
    print("{:6.1f}% ".format(subtotal/acc*100), end="")
print()


