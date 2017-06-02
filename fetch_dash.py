from enum import Enum
import dateutil.parser
import pandas as pd
import requests
import seaborn as sns


class Kind(Enum):
    PROBE = 1
    PROCESSING = 2
    TAIL = 3


headers = {
    'Accepts': 'application/json'
}
url = 'http://dashb-cms-job.cern.ch/dashboard/request.py/antasktable'


def tasks(version):
    params = {
        'user': 'Matthias Wolf',
        'task': '',
        'from': '2017-01-01 00:00',
        'to': '2019-12-31 23:59',
        'timerange': '',
        'pattern': '*crab_v{}*'.format(version)
    }
    r = requests.get(url, params=params, headers=headers)
    data = r.json()
    for task in data['antasks']:
        yield task['TASKNAME'], dateutil.parser.parse(task['TaskCreatedTS'])


def runtimes(version, tasks):
    for taskname in tasks.name:
        params = {
            'taskname': taskname,
            'what': '',
            'site': ''
        }
        r = requests.get(url, params=params, headers=headers)
        taskdata = r.json()
        for job in taskdata['taskjobs'][0]:
            if job['STATUS'] != 'finished':
                continue
            jid = job['EventRange']
            runtime = job['WrapWC'] / 60
            endtime = dateutil.parser.parse(job['finished'], dayfirst=True)
            if jid.startswith('0'):
                kind = Kind.PROBE
            elif '-' in jid:
                kind = Kind.TAIL
            else:
                kind = Kind.PROCESSING

            yield taskname, jid, kind, runtime, endtime


version = '0011'

tasks = pd.DataFrame(tasks(version))
tasks.columns = 'name submitted'.split()

jobs = pd.DataFrame(runtimes(version, tasks))
jobs.columns = 'task jobid kind runtime endtime'.split()

tasks['finished'] = [jobs[jobs.task == t].endtime.max() for t in tasks.name]
tasks['tailjobs'] = [len(jobs[(jobs.task == t) & (jobs.kind == Kind.TAIL)]) for t in tasks.name]
tasks['processingjobs'] = [len(jobs[(jobs.task == t) & (jobs.kind == Kind.PROCESSING)]) for t in tasks.name]

p = sns.distplot([d.total_seconds() / 60 for d in tasks.finished - tasks.submitted],
                 norm_hist=False,
                 rug=True, kde=False,
                 axlabel='Task Completion Time')
p.get_figure().savefig('task-completion.png')
p.get_figure().clear()

p = sns.distplot(jobs.runtime,
                 norm_hist=False,
                 rug=True, kde=False,
                 axlabel='Runtime')
p.get_figure().savefig('runtime.png')
p.get_figure().clear()
p = sns.distplot(jobs[jobs.kind == Kind.PROBE].runtime,
                 norm_hist=False,
                 rug=True, kde=False,
                 axlabel='Probe Runtime')
p.get_figure().savefig('runtime-probe.png')
p.get_figure().clear()
p = sns.distplot(jobs[jobs.kind == Kind.TAIL].runtime,
                 norm_hist=False,
                 rug=True, kde=False,
                 axlabel='Tail Runtime')
p.get_figure().savefig('runtime-tail.png')
p.get_figure().clear()
p = sns.distplot(jobs[jobs.kind == Kind.PROCESSING].runtime,
                 norm_hist=False,
                 rug=True, kde=False,
                 axlabel='Processing Runtime')
ptimes = jobs[jobs.kind == Kind.PROCESSING].sort_values('runtime').reset_index()
ptimes['quantile'] = (ptimes.index + 1) / len(ptimes)
ptimes.plot(x='runtime', y='quantile', ax=p.axes, secondary_y=True)
p.axes.right_ax.set_ylim(0, 1)
p.axes.right_ax.set_ylabel('percentile')
p.get_figure().savefig('runtime-processing.png')
p.get_figure().clear()

p = sns.violinplot(y='runtime', x='task', data=jobs)
p.get_figure().savefig('runtime-per-task.png')
p.get_figure().clear()

with sns.axes_style("white"):
    p = sns.jointplot(x="processingjobs",
                      y="tailjobs",
                      data=tasks)
    p.set_axis_labels("# of processing jobs", "# of tail jobs")
    p.fig.savefig('task-jobratio.png')
    p.fig.clear()
