# -*- coding: utf-8 -*-
"""Example django admin."""

from django_transitions.admin import WorkflowAdminMixin
from django.contrib import admin

from .models import Lifecycle


class LifecycleAdmin(WorkflowAdminMixin, admin.ModelAdmin):
    """
    Minimal Admin for Lifecycles Example.

    You probably want to make the workflow fields
    read only so yo can not change these values
    manually.

    readonly_fields = ['wf_state', 'wf_date']
    """

    list_display = ['wf_date', 'wf_state']
    list_filter = ['wf_state']


admin.site.register(Lifecycle, LifecycleAdmin)
