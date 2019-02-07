IW Python Tech Test
===================

Python version of the Infinity Works technical test. It uses the `flask`_ microframework.

.. _flask: http://flask.pocoo.org

Setting up
==========

Assumes you have cloned the repo and have Python 3 available.

Create and activate a new virtual environment::

    $ python3 -m venv venv
    $ . venv/bin/activate

Install dependencies::

    $ pip install -e .

Start the app::
    $ python app.py

Visit http://localhost:5000 to receive the application.
