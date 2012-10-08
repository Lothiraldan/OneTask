import functools
import json
import operator
import os
import time

from . import utils

from collections import namedtuple
from random import shuffle


class TaskError(RuntimeError):
    pass


class TaskCollection(object):
    """Tasks collection object."""

    def __init__(self, db_path, stdout=None):
        assert os.path.exists(db_path)
        self.db_path = db_path
        if stdout is not None:
            assert "write" in dir(stdout)
        self.stdout = stdout
        # load tasks
        try:
            self.data = json.load(open(self.db_path, 'r'))
        except (IOError, ValueError,) as err:
            raise TaskError("Unable to load tasks from db %s: %s"
                            % (self.db_path, err,))

    @classmethod
    def load(cls, db_path, **kwargs):
        """Configures and returns a collection instance from a db file.
        Asks the user to creates a new db file if none has been found.
        """
        if os.path.exists(db_path):
            return cls(db_path, **kwargs)
        print("No OneTask database file found at %s" % db_path)
        if (input("Do you want me to create one? [Yn] ").lower()
            in ("y", "",)):
            cls.create_db(db_path)
            print("Created tasks database at %s" % db_path)
            return cls(db_path, **kwargs)
        raise TaskError("Operation cancelled.")

    @classmethod
    def create_db(cls, db_path):
        "Creates a new JSON tasks db file."
        assert not os.path.exists(db_path)
        try:
            db_file = open(db_path, 'w')
            db_file.write(json.dumps(dict(tasks=[], archive=[], current=None)))
            db_file.close()
        except IOError as err:
            raise TaskError("Unable to create tasks database at %s: %s"
                            % (db_path, err))

    def add(self, title, created=None):
        "Adds a new task to the collection while keeping current active one."
        if title in [t['title'] for t in self.data['tasks']]:
            raise TaskError('Task "%s" already exists.' % title)
        task = dict(title=title, created=created or time.time())

        self.data['tasks'].append(task)

        self.update_db()
        self.notify('Task "%s" added' % title)

    def done(self, closed=None):
        "Marks current active task as done."
        if self.data['current'] is None:
            raise TaskError("No task selected.")
        task = self.data['current']

        task['closed'] = closed or time.time()
        task['duration'] = task['closed'] - task['created']
        self.data['archive'].append(task)
        self.data['current'] = None

        self.update_db()
        self.notify('Task "%s" marked as done. Completion occured in %s.'
                    % (task['title'], utils.format_duration(task['duration']),))

    def get(self):
        "Retrieves current active task."
        if self.data['current'] is None:
            if len(self.data['tasks']) == 0:
                raise TaskError("No tasks.")

            shuffle(self.data['tasks'])
            self.data['current'] = self.data['tasks'].pop()

            self.update_db()
        title = self.data['current']['title']
        self.notify(title)
        return title

    def history(self):
        "Generates a tasks completion report."
        Row = namedtuple('row', ['Created', 'Closed', 'Duration', 'Task'])
        rows = []
        durations = []
        for task in self.data['archive']:
            rows.append(Row(Created=utils.format_timestamp(task['created']),
                            Closed=utils.format_timestamp(task['closed']),
                            Duration=utils.format_duration(task['duration']),
                            Task=task['title']))
            durations.append(float(task['duration']))
        self.notify(utils.pprinttable(rows))
        self.notify("")
        average = functools.reduce(operator.add, durations) / len(durations)
        self.notify("Average task completion time: %s"
                    % utils.format_duration(average))
        self.notify("Longest:                      %s"
                    % utils.format_duration(max(durations)))
        self.notify("Shortest:                     %s"
                    % utils.format_duration(min(durations)))

    def notify(self, message):
        "Writes a message to stdout interface, if any has been provided."
        if self.stdout is not None:
            self.stdout.write("%s\n" % message)

    def skip(self):
        "Skips current active task and pull another one."
        if self.data['current'] is None:
            raise TaskError("No active task.")
        if len(self.data['tasks']) == 0:
            raise TaskError("Only one task is available. Go shopping.")
        old = self.data['current']

        shuffle(self.data['tasks'])
        self.data['current'] = self.data['tasks'].pop()
        self.data['tasks'].append(old)
        new = self.data['current']['title']

        self.update_db()
        self.notify('Switched from "%s" to "%s", good luck.' % (old['title'], new))

    def update_db(self):
        "Updates the task db with current data."
        try:
            db_file = open(self.db_path, 'w')
            db_file.write(json.dumps(self.data))
            db_file.close()
        except IOError as err:
            raise TaskError("Unable to save tasks database, sorry: %s" % err)
