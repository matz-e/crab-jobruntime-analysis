import argparse
import json
import matplotlib.pylab as plt

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

with open(args.input) as fd:
    data = json.load(fd)
    edges = [d['key'] for d in data["aggregations"]["runtime"]["runtime_inner"]["buckets"]]
    bins = [d['doc_count'] for d in data["aggregations"]["runtime"]["runtime_inner"]["buckets"]]

ax = plt.subplot(311)
ax.plot(edges, bins)
ax.set_yscale("log", nonposy='clip')
ax = plt.subplot(312)
ax.plot(edges, bins)
ax.set_xlim(0, 180)
ax = plt.subplot(313)
ax.plot(edges[60:], bins[60:])
ax.set_xlim(0, 180)

plt.savefig(args.output)
