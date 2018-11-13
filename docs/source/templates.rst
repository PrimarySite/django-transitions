Templates
==========

To use the templates you have to include ``'django_transitions'`` in
``INSTALLED_APPS`` in the projects ``settings.py`` file::

    INSTALLED_APPS = [
        'django.contrib.admin',
        ...
        'django_transitions', # this is only needed to find the templates.
    ]


The ``change_form`` template adds workflow buttons to the admin change form,
and also provides the 'save' and 'delete' buttons.
This template can be applied to the django admin class::

    change_form_template = 'transitions/change_form.html'

.. literalinclude:: ../../django_transitions/templates/transitions/change_form.html
    :language: Django

The ``read_only_change_form`` template adds workflow buttons to the admin change form,
and removes the 'save' and 'delete' buttons.
This template can be applied to the django admin class::

    change_form_template = 'transitions/read_only_change_form.html'

.. literalinclude:: ../../django_transitions/templates/transitions/read_only_change_form.html
    :language: Django
