import argparse
import dateutil.parser
import enum
import matplotlib as mpl
import matplotlib.pyplot as plt
import operator
import os
import pandas as pd
import pickle
import requests
import seaborn as sns

from bs4 import BeautifulSoup


mpl.rcParams['savefig.bbox'] = 'tight'


class Kind(enum.Enum):
    PROBE = 1
    PROCESSING = 2
    TAIL = 3


headers = {
    'Accepts': 'application/json'
}
url = 'http://dashb-cms-job.cern.ch/dashboard/request.py/antasktable'


def topusers(count):
    url = 'http://dashb-cms-job-task.cern.ch/dashboard/request.py/userssummary?range=30day'
    r = requests.get(url)
    data = BeautifulSoup(r.text, 'html.parser')
    users = []
    for row in data.find_all('tr')[2:]:
        cols = row.find_all('td')
        users.append({
            'user': cols[0].text,
            'jobs': int(cols[5].text)
        })
    users = sorted(users, key=operator.itemgetter('jobs'), reverse=True)
    return [d['user'] for d in users[:count]]


def usertasks(pattern, user, start, end):
    params = {
        'user': user,
        'task': '',
        'from': start,
        'to': end,
        'timerange': '',
        'pattern': pattern
    }
    print(f'Getting tasks submitted by {user}')
    r = requests.get(url, params=params, headers=headers)
    try:
        data = r.json()
    except Exception:
        print(f'Failed to get data for user {user}')
        return
    for task in data['antasks']:
        if task['Executable'] != 'cmsRun' or task['TaskType'] != 'analysis':
            continue
        print(f"Found task {task['TASKNAME']}")
        yield user, task['TASKNAME'], dateutil.parser.parse(task['TaskCreatedTS'])


def runtimes(tasks):
    print(f"Getting data for {len(tasks)} tasks")
    for taskname in tasks.name:
        print(f"Processing task {taskname}")
        params = {
            'taskname': taskname,
            'what': '',
            'site': ''
        }
        r = requests.get(url, params=params, headers=headers)
        taskdata = r.json()
        failed = 0
        leftover = 0
        for job in taskdata['taskjobs'][0]:
            jid = str(job['EventRange'])
            if job['STATUS'] == 'failed' and '-' in jid and not jid.startswith('0'):
                print(f"Failed: {jid}")
                failed += 1
                continue
            elif job['STATUS'] != 'finished':
                leftover += 1
                continue
            runtime = job['WrapWC'] / 60
            endtime = dateutil.parser.parse(job['finished'], dayfirst=True)
            if jid.startswith('0'):
                kind = Kind.PROBE
            elif '-' in jid:
                kind = Kind.TAIL
            else:
                kind = Kind.PROCESSING

            yield taskname, jid, kind, runtime, endtime
        if leftover == 0 and failed > 0:
            print("Task completed")


def save_plots(tasks, runtimes, outdir):
    sns.set_style("white")

    try:
        p = sns.distplot([d.total_seconds() / 60 for d in tasks.finished - tasks.submitted],
                         norm_hist=False,
                         rug=True, kde=False,
                         axlabel='Task Completion Time')
        sns.despine()
        p.get_figure().savefig(outdir + '/task-completion.png')
        p.get_figure().savefig(outdir + '/task-completion.pdf')
        p.get_figure().clear()
    except:
        pass

    p = sns.distplot(jobs.runtime,
                     norm_hist=False,
                     rug=True, kde=False,
                     axlabel='Runtime')
    sns.despine()
    p.get_figure().savefig(outdir + '/runtime.png')
    p.get_figure().savefig(outdir + '/runtime.pdf')
    p.get_figure().clear()

    if len(jobs[jobs.kind == Kind.PROBE]) > 0:
        p = sns.distplot(jobs[jobs.kind == Kind.PROBE].runtime,
                         norm_hist=False,
                         rug=True, kde=False,
                         axlabel='Probe Runtime')
        sns.despine()
        p.get_figure().savefig(outdir + '/runtime-probe.png')
        p.get_figure().savefig(outdir + '/runtime-probe.pdf')
        p.get_figure().clear()

    p = sns.distplot(jobs[jobs.kind == Kind.PROCESSING].runtime,
                     norm_hist=False,
                     rug=True, kde=False,
                     axlabel='Processing Runtime')
    ptimes = jobs[jobs.kind == Kind.PROCESSING].sort_values('runtime').reset_index()
    ptimes['percentile'] = (ptimes.index + 1) * 100 / len(ptimes)
    ptimes.plot(x='runtime', y='percentile', ax=p.axes, secondary_y=True)
    p.axes.right_ax.set_ylim(0, 100)
    p.axes.right_ax.set_ylabel('percentile')
    sns.despine(right=False)
    p.get_figure().savefig(outdir + '/runtime-processing.png')
    p.get_figure().savefig(outdir + '/runtime-processing.pdf')
    p.get_figure().clear()

    plt.close()
    oldsize = mpl.rcParams['figure.figsize']
    mpl.rcParams['figure.figsize'] = (oldsize[0] * 2, oldsize[1])
    ordered = tasks.sort_values('processingjobs').reset_index()
    ordered['plt'] = range(len(ordered))
    fig, ax = plt.subplots()
    twin = ax.twinx()
    ordered.plot(x='plt', y='processingjobs', ax=twin)
    twin.set_ylabel('Number of processing jobs')
    p = sns.boxplot(y='runtime', x='task', ax=ax, data=jobs[jobs.kind == Kind.PROCESSING], order=ordered.name)
    p.set(xticklabels=[])
    sns.despine(bottom=True, right=False)
    p.get_figure().savefig(outdir + '/runtime-processing-per-task.png')
    p.get_figure().savefig(outdir + '/runtime-processing-per-task.pdf')
    p.get_figure().clear()
    mpl.rcParams['figure.figsize'] = oldsize
    plt.close()

    if len(jobs[jobs.kind == Kind.TAIL]) > 0:
        p = sns.distplot(jobs[jobs.kind == Kind.TAIL].runtime,
                         norm_hist=False,
                         rug=True, kde=False,
                         axlabel='Tail Runtime')
        sns.despine()
        p.get_figure().savefig(outdir + '/runtime-tail.png')
        p.get_figure().savefig(outdir + '/runtime-tail.pdf')
        p.get_figure().clear()

        p = sns.jointplot(x="processingjobs",
                          y="tailjobs",
                          data=tasks)
        p.set_axis_labels("# of processing jobs", "# of tail jobs")
        sns.despine()
        p.fig.savefig(outdir + '/task-jobratio.png')
        p.fig.savefig(outdir + '/task-jobratio.pdf')
        p.fig.clear()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='plot data from dashboard')
    parser.add_argument('--start', default='2017-01-01 00:00',
                        help='start timestamp for search')
    parser.add_argument('--end', default='2019-01-01 00:00',
                        help='final timestamp for search')
    parser.add_argument('--topusers', default=None, type=int, metavar='N',
                        help='get tasks for top N users')
    parser.add_argument('--user', default=['Matthias Wolf'], nargs='*',
                        help='user to query the database for')
    parser.add_argument('--update', default=False, action='store_true',
                        help='update cached data')
    parser.add_argument('pattern',
                        help='pattern to use when querying the database')
    parser.add_argument('outdir',
                        help='directory to save the output to')
    args = parser.parse_args()

    if args.topusers is not None:
        args.user = topusers(args.topusers)
        print(f'Getting data for users {args.user}')

    cachefile = args.outdir + '.pkl'
    if args.update or not os.path.exists(cachefile):
        tasks = None
        for user in args.user:
            ts = pd.DataFrame(usertasks(args.pattern, user, args.start, args.end))
            if len(ts) == 0:
                continue
            ts.columns = 'user name submitted'.split()
            if tasks is None:
                tasks = ts
            else:
                tasks = tasks.append(ts)

        jobs = pd.DataFrame(runtimes(tasks))
        jobs.columns = 'task jobid kind runtime endtime'.split()

        tasks['finished'] = [jobs[jobs.task == t].endtime.max() for t in tasks.name]
        tasks['tailjobs'] = [len(jobs[(jobs.task == t) & (jobs.kind == Kind.TAIL)]) for t in tasks.name]
        tasks['processingjobs'] = [len(jobs[(jobs.task == t) & (jobs.kind == Kind.PROCESSING)]) for t in tasks.name]

        with open(cachefile, 'wb') as fd:
            pickle.dump((jobs, tasks), fd)
    else:
        with open(cachefile, 'rb') as fd:
            jobs, tasks = pickle.load(fd)

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    save_plots(tasks, runtimes, args.outdir)
