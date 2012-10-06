# -*- coding: utf-8 -*-

import json
import tempfile
import unittest

from collection import TaskCollection


class TaskCollectionTest(unittest.TestCase):
    def _load(self, tasks):
        temp = tempfile.NamedTemporaryFile(prefix='onetasktest', suffix='.json')
        temp.write(json.dumps(tasks))
        temp.read()
        return TaskCollection.load(temp.name)

    def test_load(self):
        tasks = self._load(["task1", "task2"])
        self.assertEquals(len(tasks), 2)
        self.assertEquals(tasks[0], 'task1')
        self.assertEquals(tasks[1], 'task2')

    def test_add(self):
        tasks = self._load([])
        tasks.add('task1')
        self.assertEquals(len(tasks), 1)
        self.assertEquals(tasks[0], 'task1')
        tasks.add('task2')
        self.assertEquals(len(tasks), 2)
        self.assertEquals(tasks[0], 'task1')
        tasks.add('task3')
        self.assertEquals(len(tasks), 3)
        self.assertEquals(tasks[0], 'task1')

    def test_get(self):
        tasks = self._load(["task1"])
        for x in xrange(2, 100):
            tasks.add('task%d' % x)
            self.assertEqual(len(tasks), x)
            self.assertEquals(tasks.get(), 'task1')
        tasks.done()
        self.assertEqual(len(tasks), x - 1)
        self.assertNotEquals(tasks.get(), 'task1')

    def test_done(self):
        tasks = self._load([])
        tasks.add('task1')
        self.assertEquals(tasks.get(), 'task1')
        self.assertEquals(len(tasks), 1)
        tasks.add('task2')
        self.assertEquals(tasks.get(), 'task1')
        self.assertEquals(len(tasks), 2)
        tasks.done()
        self.assertEquals(len(tasks), 1)
        self.assertEquals(tasks[0], 'task2')


if __name__ == '__main__':
    unittest.main()
