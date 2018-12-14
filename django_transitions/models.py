# -*- coding: utf-8 -*-
"""An opinonated example for a workflow mixin."""

# Django
from django.db import models
from django.utils import timezone

# Local
from .workflow import StatusBase


class WorkflowMigrationMixin(models.Model):
    """
    A mixin to provide workflow state and workflow date fields.

    This is a minimal example implementation.
    """

    class Meta:  # noqa: D106
        abstract = True

    wf_state = models.CharField(
        verbose_name='Workflow Status',
        null=False,
        blank=False,
        default=StatusBase.SM_INITIAL_STATE,
        choices=StatusBase.STATE_CHOICES,
        max_length=32,
        help_text='Workflow state',
    )

    wf_date = models.DateTimeField(
        verbose_name='Workflow Date',
        null=False,
        blank=False,
        default=timezone.now,
        help_text='Indicates when this workflowstate was entered.',
    )
