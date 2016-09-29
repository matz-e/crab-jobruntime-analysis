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
ax2.set_xlim(0, 600)
ax2.set_ylabel("# jobs")
plt.setp(ax2.get_xticklabels(), visible=False)
ax3 = plt.subplot(513, sharex=ax2)
ax3.grid(True)
ax3.plot(edges[60:], bins[60:])
ax3.set_xlim(0, 600)
ax3.set_ylabel("# jobs > 1h")
plt.setp(ax3.get_xticklabels(), visible=False)
ax4 = plt.subplot(514, sharex=ax2)
ax4.grid(True)
ax4.plot(edges, cummulative * 1. / grandtotal)
ax4.set_xlim(0, 600)
ax4.set_ylabel("job fraction")
plt.setp(ax4.get_xticklabels(), visible=False)
ax5 = plt.subplot(515, sharex=ax2)
ax5.grid(True)
ax5.plot(edges, sumruntimes * 1. / grandruntime)
ax5.set_xlabel("runtime / m")
ax5.set_xlim(0, 600)
ax5.set_ylabel("runtime fraction")

plt.savefig(args.output)

basename, ext = args.output.rsplit('.', 1)

for xmax in (240, 400, 800):
    plt.figure(figsize=(6, 5))

    ax6 = plt.subplot(111)
    ax6.grid(True)
    ax6.plot(edges, cummulative * 100. / grandtotal)
    ax6.set_xlim(0, xmax)
    ax6.set_ylabel("jobs / %")
    ax6.set_xlabel("max job runtime / m")
    ax6.set_title("Fraction of jobs with maximum runtime")

    plt.savefig('{}_{}_{}.{}'.format(basename, 'jobfraction', xmax, ext))

    plt.figure(figsize=(6, 5))

    ax7 = plt.subplot(111)
    ax7.grid(True)
    ax7.plot(edges, bins)
    ax7.set_ylabel("# jobs")
    ax7.set_yscale("log", nonposy='clip')
    ax7.set_xlabel("job runtime / m")
    ax7.set_xlim(0, xmax)
    ax7.set_title("Job distribution w.r.t. runtime")

    plt.savefig('{}_{}_{}.{}'.format(basename, 'jobruntime_log', xmax, ext))

    plt.figure(figsize=(6, 5))

    ax8 = plt.subplot(111)
    ax8.grid(True)
    ax8.plot(edges, bins)
    ax8.set_ylabel("# jobs")
    ax8.set_xlabel("job runtime / m")
    ax8.set_xlim(0, xmax)
    ax8.set_title("Job distribution w.r.t. runtime")

    plt.savefig('{}_{}_{}.{}'.format(basename, 'jobruntime', xmax, ext))
