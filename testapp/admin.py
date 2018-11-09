# -*- coding: utf-8 -*-
"""Example django admin."""

from django_transitions.admin import WorkflowAdminMixin
from django.contrib import admin

from .models import Lifecycle

@admin.register()
class LifecycleAdmin(WorkflowAdminMixin, admin.ModelAdmin):
    """Minimal Admin for Lifecycles"""

    list_display = ['wf_date', 'wf_status']
    list_filter = ['wf_status']


admin.site.register(Lifecycle, LifecycleAdmin)
