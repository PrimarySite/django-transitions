django-transitions
====================

.. inclusion-marker-do-not-remove

A wrapper of pytransitions_ for django_

.. image:: https://circleci.com/gh/PrimarySite/django-transitions.svg?style=svg
    :target: https://circleci.com/gh/PrimarySite/django-transitions
    :alt: Test Status

.. image:: https://codecov.io/gh/PrimarySite/django-transitions/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/PrimarySite/django-transitions
    :alt: Test Coverage

.. image:: https://readthedocs.org/projects/django-transitions/badge/?version=latest
    :target: https://django-transitions.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

You do not *need* django-transitions to integrate django_ and pytransitions_.
It is meant to be a lightweight wrapper (it has just over 50 logical lines of code)
and documentation how to go about using pytransitions inside a django application.

This package provides:

- Example workflow implementation.
- Base classes and mixins to
    - Keep it DRY
    - Keep transitions consistent
    - Reduce cut and paste
    - Avoid boiler plate.
- Admin mixin to add workflow actions to the django admin.
- Admin templates


.. _django: https://www.djangoproject.com/
.. _pytransitions: https://pypi.org/project/transitions/
