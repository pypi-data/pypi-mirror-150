=====
popro
=====


.. image:: https://img.shields.io/pypi/v/popro.svg
        :target: https://pypi.python.org/pypi/popro

.. image:: https://img.shields.io/travis/derycck/popro.svg
        :target: https://travis-ci.com/derycck/popro

.. image:: https://readthedocs.org/projects/popro/badge/?version=latest
        :target: https://popro.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




A population projection engine


* Free software: MIT license
* Documentation: https://popro.readthedocs.io.


Features
--------

* Calculates population projection segmented by age over the years
         * Inputs:
                 * Specific year census database (place, age, population)
                 * Database of people born over the years (year, place, births)
                 * Projected population database not segmented by age over the years (year, place, population)
         * Output:
                 * Population projection segmented by age database (year, place, age, population)
                 * Errors report on combination of "place, age, year" unable to forecast (year, place, age, error_msg)

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
