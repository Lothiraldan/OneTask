import json
import os

from collections import deque
from random import shuffle


class TaskError(RuntimeError):
    pass


class TaskCollection(deque):
    """Tasks collection object."""

    def __init__(self, db_path):
        self.db_path = db_path
        # load tasks
        try:
            tasks_list = json.load(open(self.db_path, 'r'))
        except (IOError, ValueError,), err:
            raise TaskError(u"Unable to load tasks from db %s: %s"
                            % (self.db_path, err,))
        super(TaskCollection, self).__init__(tasks_list)

    @classmethod
    def load(cls, db_path):
        """Configures and returns a collection instance from a db file.
        Asks the user to creates a new db file if none has been found.
        """
        if os.path.exists(db_path):
            return cls(db_path)
        print u"No OneTask database file found at %s" % db_path
        if (raw_input(u"Do you want me to create one? [Yn] ").lower()
            in ("y", "",)):
            cls.create_db(db_path)
            return cls(db_path)
        raise TaskError(u"Operation cancelled.")

    @classmethod
    def create_db(cls, db_path):
        "Creates a new JSON tasks db file."
        assert not os.path.exists(db_path)
        try:
            db_file = open(db_path, 'w')
            db_file.write('[]')
            db_file.close()
        except IOError, err:
            raise TaskError(u"Unable to create tasks database at %s: %s"
                            % (db_path, err))
        print u"Created tasks database at %s" % db_path

    def add(self, task):
        "Adds a new task to the collection while keeping current active one."
        if task in self:
            raise TaskError(u'Task "%s" already exists.' % task)
        if len(self) > 0:
            # pop current active task
            active = self.popleft()
            # shuffle rest
            shuffle(self)
            # add new task
            self.append(task)
            # restore active tasks
            self.appendleft(active)
        else:
            self.append(task)
        self.update_db()
        print u'Task "%s" added' % task

    def done(self):
        "Marks current active task as done."
        try:
            task = self.popleft()
        except IndexError:
            raise TaskError(u"Empty task list.")
        shuffle(self)
        self.update_db()
        print u'Task "%s" marked as done' % task

    def get(self):
        "Retrieves current active task."
        if len(self) == 0:
            raise TaskError(u"No tasks.")
        print self[0]
        return self[0]

    def update_db(self):
        "Updates the task db with current data."
        try:
            db_file = open(self.db_path, 'w')
            db_file.write(json.dumps(list(self)))
            db_file.close()
        except IOError, err:
            raise TaskError(u"Unable to save tasks database, sorry: %s" % err)
