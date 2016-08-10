import argparse
import json
import matplotlib
import matplotlib.pylab as plt

matplotlib.rc('axes.formatter', limits=(-3, 4))

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

with open(args.input) as fd:
    data = json.load(fd)
    edges = [d['key'] for d in data["aggregations"]["runtime"]["runtime_inner"]["buckets"]]
    bins = [d['doc_count'] for d in data["aggregations"]["runtime"]["runtime_inner"]["buckets"]]

ax1 = plt.subplot(311)
ax1.plot(edges, bins)
ax1.set_yscale("log", nonposy='clip')
ax1.set_ylabel("# jobs")
ax2 = plt.subplot(312)
ax2.plot(edges, bins)
ax2.set_xlim(0, 180)
ax2.set_ylabel("# jobs")
plt.setp(ax2.get_xticklabels(), visible=False)
ax3 = plt.subplot(313, sharex=ax2)
ax3.plot(edges[60:], bins[60:])
ax3.set_xlabel("runtime")
ax3.set_xlim(0, 180)
ax3.set_ylabel("# jobs > 1h")

plt.savefig(args.output)
