import requests

def runtimes(version):
    params = {
        'user': 'Matthias Wolf',
        'task': '',
        'from': '2016-07-01 00:00',
        'to': '2017-02-06 23:59',
        'timerange': '',
        'pattern': '*crab_v{}*'.format(version)
    }
    headers = {
        'Accepts': 'application/json'
    }
    url = 'http://dashb-cms-job.cern.ch/dashboard/request.py/antasktable'

    r = requests.get(url, params=params, headers=headers)

    data = r.json()

    for task in data['antasks']:
        taskname = task['TASKNAME']

        params = {
            'taskname': taskname,
            'what': '',
            'site': ''
        }

        r2 = requests.get(url, params=params, headers=headers)
        taskdata = r2.json()
        for job in taskdata['taskjobs'][0]:
            if job['JobExecExitCode'] == 0:
                yield job['WrapWC']


import numpy as np
import pickle

data34 = np.array(list(runtimes(34)))

with open('responses/data.34', 'wb') as fd:
    pickle.dump(data34, fd)
