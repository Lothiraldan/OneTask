OneTask: Manage task, one task at the time
==========================================

**OneTask** let you focus on one task at the time, avoiding discouragement by seing all the remaining work to do.

Build status: |build_status|

.. |build_status| image:: https://secure.travis-ci.org/Lothiraldan/OneTask.png
    :target: http://travis-ci.org/Lothiraldan/OneTask

Requirements
------------

There's none expect a working Python 2.7+ or 3.2+ installation.

Installation
------------

Right now installation is done using ``git``::

    $> git clone https://github.com/Lothiraldan/OneTask.git
    $> python OneTask/setup.py install

Expect a Pypi package soon though.

QuickStart
----------

- Add a task::

    $> onetask add 'Create onetask'
    Task "Create onetask" added

- Get a random task::

    $> onetask get
    Create onetask

If you try to get another task, you will get the same one.

- Mark current task as done::

    $> onetask done
    Task "Create onetask" marked as done

    $> onetask get
    Empty task list.

Sometimes you may want to skip this horrible task you *know* you can't do right now, but want to keep in the list::

    $> onetask skip
    Switched from "task2" to "task3", good luck.

Last, you probably feel like contemplating accomplished work::

    $> onetask history

That can give some nice output like the one below:

.. image:: http://cl.ly/image/3Y3c0w071y14/Capture%20d%E2%80%99%C3%A9cran%202012-10-06%20%C3%A0%2022.38.36.png

Tests
-----

To run OneTask's test suite, a dedicated command is available::

    $> onetask test

In case anything fails, feel free to `open an issue about it <https://github.com/Lothiraldan/OneTask/issues/new>`_.

Features
--------

- OneTask has **no** synchronization between multiple devices.
- OneTask has **no** web interface.
- OneTask has **no** web API.
- OneTask has **no** social features.
- OneTask has **no** collaboration features.
- OneTask has **no** GUI.
- OneTask has **no** cofee maker capability.
- OneTask has **no** speech-to-text feature.
- OneTask has **no** text-to-speech feature.
- OneTask has **no** other todo manager export/import.
- OneTask has **no** task search option.
- OneTask has **no** deadline features.
- OneTask has **no** widget option.
- OneTask has **no** pro option.
- OneTask has **no** ads.
- OneTask has **no** distraction free option.
- OneTask has **no** kawaii colors.
- OneTask has **no** retina display.
- OneTask has **no** repeating tasks.
- OneTask has **no** alerts.
- OneTask has **no** tasks.

OneTask is a minimalist task manager and that's just fine.
