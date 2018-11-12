Templates
----------

To use the templates you have to include 'django_transitions' in
`INSTALLED_APPS` in the projects `settings.py` file::

    INSTALLED_APPS = [
        'django.contrib.admin',
        ...
        'django_transitions', # this is only needed to find the templates.
    ]


This template can be applied to the django admin class::

    change_form_template = 'transitions/change_form.html'

.. literalinclude:: ../../django_transitions/templates/transitions/change_form.html
