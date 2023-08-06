.. highlight:: python

*****************
Development notes
*****************

Getting ready
=============

This section will help you with the steps needed to start working on |project|.

1. Clone the repository:

   .. prompt:: bash
      :substitutions:

      git clone |repo_url|

2. CD into in:

   .. prompt:: bash

      cd pacbio-data-processing

3. (optional) Create a virtualenv/venv and activate it. See instructions in
   :ref:`installation`.
4. Install flit:

   .. prompt:: bash

      pip install flit

5. Install |project| with all the optional dependencies:

   .. prompt:: bash

      flit install --symlink --deps=develop

With this, you should be ready to start coding but... please, keep reading!


Testing
=======

The development of |project| follows the **double loop TDD** approach.
See `double loop TDD`_.


Writing code
------------

`double loop TDD`_ is a generalization of plain TDD.  A *second TDD loop* is added to
the procedure. This sencond loop is *behaviour driven*, meaning that the functionality
is guiding us in the development process.

In brief, the procedure to develop code with this technique is as follows:

1. Write a functional test case (aka acceptance test) for the functionality you
   want to implement. You do this from the point of view of the *user*. After this
   step you will have a failing FT for that feature.
2. Make your FT pass by implementing the needed features in your code following a
   normal TDD approach. Your point of view is now different from point 1: you
   look at the problem as a developer. Do not implement more features in your code
   than your FT requires to pass. In this phase we are just playing the usual TDD
   game with the goal of making the FT for the current feature pass.
   

.. _`double loop TDD`: http://coding-is-like-cooking.info/2013/04/outside-in-development-with-double-loop-tdd/


Running the tests
-----------------

* For the functional tests

  .. code-block:: console

     $ pytest tests/functional

* Unit tests (with coverage)

  .. code-block:: console

     $ pytest --cov=pacbio_data_processing tests/unit pacbio_data_processing


Writing tests
-------------

The FTs rely on ``pytest`` (with fixtures; without stdlib's unittest)

The UTs use ``unittest`` from the standard library.


GUI
---

In a first approximation, the GUI tests were a bit smoky. The tests
consisted in:

1. (FTs) Ensure that if ``sm-analysis-gui`` is launched, a process
   remains there for some time (as one would expect after launching
   a gui program).
2. (UTs) Mocky tests to check that Gooey has been employed.
   
One improvemnet would be using something like ``PyAutoGUI``.

