# -*- coding: utf-8 -*-

import json
import tempfile
import unittest

from .collection import TaskCollection


class TaskCollectionTest(unittest.TestCase):
    def _load(self, **kwargs):
        temp = tempfile.NamedTemporaryFile(prefix='onetasktest', suffix='.json')
        temp.write(bytes(json.dumps(dict(**kwargs)), 'UTF-8'))
        temp.read()
        return TaskCollection.load(temp.name)

    def test_load(self):
        tasks = self._load(tasks=[{"title": "task1"}, {"title": "task2"}])
        self.assertEquals(len(tasks.data['tasks']), 2)
        self.assertEquals(tasks.data['tasks'][0]['title'], 'task1')
        self.assertEquals(tasks.data['tasks'][1]['title'], 'task2')

    def test_add(self):
        tasks = self._load(tasks=[])
        tasks.add('task1')
        self.assertEquals(len(tasks.data['tasks']), 1)
        self.assertEquals(tasks.data['tasks'][0]['title'], 'task1')
        tasks.add('task2')
        self.assertEquals(len(tasks.data['tasks']), 2)
        self.assertEquals(tasks.data['tasks'][0]['title'], 'task1')
        tasks.add('task3')
        self.assertEquals(len(tasks.data['tasks']), 3)
        self.assertEquals(tasks.data['tasks'][0]['title'], 'task1')

    def test_get(self):
        tasks = self._load(tasks=[{"title": "task1", "created": 1000}],
            current=None, archive=[])
        self.assertEqual(tasks.get(), 'task1')
        for x in range(2, 100):
            tasks.add('task%d' % x)
            self.assertEqual(len(tasks.data['tasks']), x - 1)
            self.assertEquals(tasks.get(), 'task1')
        tasks.done(closed=3000)
        self.assertEqual(len(tasks.data['tasks']), x - 1)
        self.assertNotEquals(tasks.get(), 'task1')
        self.assertEquals(tasks.data['archive'][0]['title'], 'task1')
        self.assertEquals(tasks.data['archive'][0]['duration'], 2000)

    def test_done(self):
        tasks = self._load(tasks=[], current=None, archive=[])
        tasks.add('task1')
        self.assertEquals(tasks.get(), 'task1')
        self.assertEquals(len(tasks.data['tasks']), 0)
        tasks.add('task2')
        self.assertEquals(tasks.get(), 'task1')
        self.assertEquals(len(tasks.data['tasks']), 1)
        self.assertEquals(len(tasks.data['archive']), 0)
        tasks.done()
        self.assertEquals(len(tasks.data['tasks']), 1)
        self.assertEquals(tasks.data['tasks'][0]['title'], 'task2')
        self.assertEquals(len(tasks.data['archive']), 1)
        self.assertEquals(tasks.data['archive'][0]['title'], 'task1')
        tasks.get()
        tasks.done()
        self.assertEquals(len(tasks.data['tasks']), 0)
        self.assertEquals(len(tasks.data['archive']), 2)
        self.assertEquals(tasks.data['archive'][0]['title'], 'task1')
        self.assertEquals(tasks.data['archive'][1]['title'], 'task2')

    def test_skip(self):
        tasks = self._load(tasks=[{"title": "task1"},
                                  {"title": "task2"},
                                  {"title": "task3"}],
                           current=None)
        current = tasks.get()
        for i in range(4):
            tasks.skip()
            new = tasks.get()
            self.assertNotEquals(current, new)
            current = new


if __name__ == '__main__':
    unittest.main()
