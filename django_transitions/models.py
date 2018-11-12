# -*- coding: utf-8 -*-
"""An opinonated example for a workflow mixin."""

# Django
from django.db import models


class WorkflowMigrationMixin(models.Model):
    """
    A mixin to provide workflow state and workflow date fields.

    This is a minimal example implementation.
    """

    class Meta:  # noqa: D106
        abstract = True

    wf_state = models.CharField(
        verbose_name='Workflow Status',
        null=True,
        blank=True,
        max_length=32,
        help_text='Workflow state',
    )

    wf_date = models.DateTimeField(
        verbose_name='Workflow Date',
        null=True,
        blank=True,
        help_text='Indicates when this workflowstate was entered.',
    )
