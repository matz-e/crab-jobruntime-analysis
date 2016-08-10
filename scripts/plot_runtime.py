import argparse
import json
import matplotlib
import matplotlib.pylab as plt
import numpy as np

matplotlib.rc('axes.formatter', limits=(-3, 4))

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

with open(args.input) as fd:
    data = json.load(fd)
    edges = [d['key'] for d in data["aggregations"]["runtime"]["runtime_inner"]["buckets"]]
    bins = [d['doc_count'] for d in data["aggregations"]["runtime"]["runtime_inner"]["buckets"]]

cummulative = np.cumsum(bins)
grandtotal = np.sum(bins)

runtimes = np.multiply(edges, bins)
sumruntimes = np.cumsum(runtimes)
grandruntime = np.sum(runtimes)

plt.figure(figsize=(10, 12))

ax1 = plt.subplot(511)
ax1.plot(edges, bins)
ax1.set_yscale("log", nonposy='clip')
ax1.set_ylabel("# jobs")
ax2 = plt.subplot(512)
ax2.grid(True)
ax2.plot(edges, bins)
ax2.set_xlim(0, 180)
ax2.set_ylabel("# jobs")
plt.setp(ax2.get_xticklabels(), visible=False)
ax3 = plt.subplot(513, sharex=ax2)
ax3.grid(True)
ax3.plot(edges[60:], bins[60:])
ax3.set_xlim(0, 180)
ax3.set_ylabel("# jobs > 1h")
plt.setp(ax3.get_xticklabels(), visible=False)
ax4 = plt.subplot(514, sharex=ax2)
ax4.grid(True)
ax4.plot(edges, cummulative * 1. / grandtotal)
ax4.set_xlim(0, 180)
ax4.set_ylabel("job fraction")
plt.setp(ax4.get_xticklabels(), visible=False)
ax5 = plt.subplot(515, sharex=ax2)
ax5.grid(True)
ax5.plot(edges, sumruntimes * 1. / grandruntime)
ax5.set_xlabel("runtime / m")
ax5.set_xlim(0, 180)
ax5.set_ylabel("runtime fraction")

plt.savefig(args.output)
