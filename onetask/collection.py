import json
import os
import time

import utils

from collections import deque, namedtuple
from random import shuffle


class TaskError(RuntimeError):
    pass


class TaskCollection(object):
    """Tasks collection object."""
    tasks = deque()
    archive = deque()

    def __init__(self, db_path, stdout=None):
        assert os.path.exists(db_path)
        self.db_path = db_path
        if stdout is not None:
            assert "write" in dir(stdout)
        self.stdout = stdout
        # load tasks
        try:
            tasks_data = json.load(open(self.db_path, 'r'))
        except (IOError, ValueError,), err:
            raise TaskError(u"Unable to load tasks from db %s: %s"
                            % (self.db_path, err,))
        self.tasks = deque(tasks_data.get('tasks', []))
        self.archive = deque(tasks_data.get('archive', []))

    @classmethod
    def load(cls, db_path, **kwargs):
        """Configures and returns a collection instance from a db file.
        Asks the user to creates a new db file if none has been found.
        """
        if os.path.exists(db_path):
            return cls(db_path, **kwargs)
        print u"No OneTask database file found at %s" % db_path
        if (raw_input(u"Do you want me to create one? [Yn] ").lower()
            in ("y", "",)):
            cls.create_db(db_path)
            print u"Created tasks database at %s" % db_path
            return cls(db_path, **kwargs)
        raise TaskError(u"Operation cancelled.")

    @classmethod
    def create_db(cls, db_path):
        "Creates a new JSON tasks db file."
        assert not os.path.exists(db_path)
        try:
            db_file = open(db_path, 'w')
            db_file.write(json.dumps(dict(tasks=[], archive=[]), indent=4))
            db_file.close()
        except IOError, err:
            raise TaskError(u"Unable to create tasks database at %s: %s"
                            % (db_path, err))

    def add(self, title, created=None):
        "Adds a new task to the collection while keeping current active one."
        if title in [t['title'] for t in self.tasks]:
            raise TaskError(u'Task "%s" already exists.' % title)
        task = dict(title=title, created=created or time.time())
        if len(self.tasks) > 0:
            # pop current active task
            active = self.tasks.popleft()
            # shuffle rest
            shuffle(self.tasks)
            # add new task
            self.tasks.append(task)
            # restore active tasks
            self.tasks.appendleft(active)
        else:
            self.tasks.append(task)
        self.update_db()
        self.notify(u'Task "%s" added' % title)

    def done(self, closed=None):
        "Marks current active task as done."
        try:
            task = self.tasks.popleft()
        except IndexError:
            raise TaskError(u"Empty task list.")
        shuffle(self.tasks)
        task['closed'] = closed or time.time()
        task['duration'] = task['closed'] - task['created']
        self.archive.appendleft(task)
        self.update_db()
        self.notify(u'Task "%s" marked as done. Completion occured in %s.'
                    % (task['title'], utils.format_duration(task['duration']),))

    def get(self):
        "Retrieves current active task."
        if len(self.tasks) == 0:
            raise TaskError(u"No tasks.")
        title = self.tasks[0]['title']
        self.notify(title)
        return title

    def history(self):
        "Generates a tasks completion report."
        Row = namedtuple('row', ['Created', 'Closed', 'Duration', 'Task'])
        rows = []
        for task in self.archive:
            rows.append(Row(Created=utils.format_timestamp(task['created']),
                            Closed=utils.format_timestamp(task['closed']),
                            Duration=utils.format_duration(task['duration']),
                            Task=task['title']))
        self.notify(utils.pprinttable(rows))

    def notify(self, message):
        "Writes a message to stdout interface, if any has been provided."
        if self.stdout is not None:
            self.stdout.write("%s\n" % message)

    def skip(self):
        "Skips current active task."
        # XXX
        pass

    def update_db(self):
        "Updates the task db with current data."
        try:
            db_file = open(self.db_path, 'w')
            db_file.write(json.dumps(dict(tasks=list(self.tasks),
                                          archive=list(self.archive)),
                          indent=4))
            db_file.close()
        except IOError, err:
            raise TaskError(u"Unable to save tasks database, sorry: %s" % err)
