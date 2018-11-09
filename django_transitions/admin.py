# -*- coding: utf-8 -*-
"""Mixins for the django admin."""
from django.contrib import messages
from django.http import HttpResponseRedirect

class WorkflowAdminMixin(object):
    """"
    A mixin to provide workflow transition actions.

    This imlementation assumes that the field to store your
    workflowstate is called wf_state.

    It will create an admin log entry.
    """

    change_form_template = 'transitions/change_form.html'

    def response_change(self, request, obj):
        """Add actions for the workflow events."""
        events = list(obj.get_available_events())
        for event in events:
            if '_' + event['transition'].name not  in request.POST:
                continue

            before = obj.wf_state
            if getattr(obj, event['transition'].name)():
                obj.save()
                after = obj.wf_state
                message = 'Status changed from {0} to {1} by transition {2}'.format(
                    before, after, event['transition'].name)
                self.message_user(request, message, messages.SUCCESS)
                self.log_change(request, obj, message)
            else:
                message = 'Status could not be changed from {0} by transition {1}'.format(
                    before, event['transition'].name)
                self.message_user(request, message, messages.ERROR)
            return HttpResponseRedirect('.')
        return super(WorkflowAdminMixin, self).response_change(request, obj)
