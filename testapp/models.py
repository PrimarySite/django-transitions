# -*- coding: utf-8 -*-
"""Django transitions."""

from django.db import models
from django.utils import timezone

from .workflows import LiveStatus
from .workflows import LifecycleStateMachineMixin


class Lifecycle(LifecycleStateMachineMixin, models.Model):
    """
    A model that provides workflow state and workflow date fields.

    This is a minimal example implementation.
    """

    class Meta:  # noqa: D106
        abstract = False

    wf_state = models.CharField(
        verbose_name = 'Workflow Status',
        null=False,
        blank=False,
        default=LiveStatus.SM_INITIAL_STATE,
        choices=LiveStatus.STATE_CHOICES,
        max_length=32,
        help_text='Workflow state',
    )

    wf_date =  models.DateTimeField(
        verbose_name = 'Workflow Date',
        null=False,
        blank=False,
        default=timezone.now,
        help_text='Indicates when this workflowstate was entered.',
    )
