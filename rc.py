#!/usr/bin/env python
'''A dumb-as-rocks recurring checklist manager.

You can add events and set them to repeat a number of days after completion.
>>> add("Scrub toilets", interval=14)

Then you can flag it as completed, for now.
>>> complete("Scrub toilets")

It will show up in the listing as to be done in its next interval.
>>> checklist()
['[ ] Scrub toilets (in 13 days.)']

'''

import datetime
from dateutil.relativedelta import relativedelta
import jsonpickle

def _load(filename='rc.jpkl'):
    try:
        with open(filename, 'r') as f:
            return jsonpickle.decode(f.read())
    except (IOError):
        return dict(tasks=list())

def _save(db, filename='rc.jpkl'):
    with open(filename, 'w') as f:
        return f.write(jsonpickle.encode(db))


def add(name, interval=7):
    '''Add a task and set it to repeat every `interval` days.'''
    db = _load()
    next_date = datetime.datetime.now() + relativedelta(days=interval)
    db['tasks'].append(dict(name=name, interval=interval, next_date=next_date))
    _save(db)

def complete(task):
    db = _load()
    for i, t in enumerate(db['tasks']):
        if t['name'] == task:
            interval = t['interval']
            db['tasks'][i]['next_date'] = datetime.datetime.now() + relativedelta(days=interval)
            break
    else:
        return "Task not found."

    _save(db)

def checklist():
    db = _load()
    result = []
    for t in db['tasks']:
        next_date = t['next_date']
        if next_date > datetime.datetime.today():
            # If in the future, use "in"
            interval = "in {days} days.".format(days=(next_date-datetime.datetime.today()).days)
        elif next_date < datetime.datetime.today():
            # If in the past, use "ago"
            interval = "{days} days ago.".format(days=(datetime.datetime.today()-next_date).days)
        else:
            # If today, just use "today".
            interval = "Today"
        result.append("[ ] {name} ({interval})".format(name=t['name'], interval=interval))

    return result
