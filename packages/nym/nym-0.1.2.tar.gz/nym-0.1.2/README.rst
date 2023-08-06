===
nym
===


.. image:: https://img.shields.io/pypi/v/nym.svg
        :target: https://pypi.python.org/pypi/nym

.. image:: https://img.shields.io/travis/gmagno/nym.svg
        :target: https://travis-ci.com/gmagno/nym

.. image:: https://readthedocs.org/projects/nym/badge/?version=latest
        :target: https://nym.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Nim extension for Python using nimporter, example project.


* Free software: MIT license
* Documentation: https://nym.readthedocs.io.


Usage
-----

To install nym, run this command in your terminal:

.. code-block:: console

    $ pip install nym


To install from source:

.. code-block:: console

    $ git clone git@github.com:gmagno/nym.git && cd nym
    $ python -m venv .venv
    $ source .venv/bin/activate
    $ pip install -U pip && pip install -r requirements_dev.txt
    $ python -m nym.cli


To build:

.. code-block:: console

    $ make dist


To use nym:

.. code-block:: python

    from nym import fast, slow

    start = time.time()
    python_ret = slow.fib(33)
    python_time = time.time() - start

    restart = time.time()
    nim_ret = fast.fib(33)
    nim_time = time.time() - restart

    print(f"python ret: {python_ret}")
    print(f"python elapsed time: {python_time}")

    print(f"nim ret: {nim_ret}")
    print(f"nim elapsed time: {nim_time}")
