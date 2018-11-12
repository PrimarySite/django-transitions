# -*- coding: utf-8 -*-
"""Mixins for the django admin."""
# Django
from django.contrib import messages
from django.http import HttpResponseRedirect


class WorkflowAdminMixin(object):
    """
    A mixin to provide workflow transition actions.

    It will create an admin log entry.
    """

    change_form_template = 'transitions/change_form.html'

    def response_change(self, request, obj):
        """Add actions for the workflow events."""
        events = list(obj.get_available_events())
        for event in events:
            if '_' + event['transition'].name not in request.POST:
                continue

            before = obj.state
            if getattr(obj, event['transition'].name)():
                obj.save()
                after = obj.state
                message = ('Status changed from {0} to {1} by transition {2}'
                           .format(before, after, event['transition'].name))
                self.message_user(request, message, messages.SUCCESS)
                self.log_change(request, obj, message)
            else:
                message = ('Status could not be changed from '
                           '{0} by transition {1}'
                           .format(before, event['transition'].name))
                self.message_user(request, message, messages.ERROR)
            return HttpResponseRedirect('.')
        return super(WorkflowAdminMixin, self).response_change(request, obj)
