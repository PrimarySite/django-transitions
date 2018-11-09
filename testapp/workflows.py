# -*- coding: utf-8 -*-
"""Example Lifecycle workflow."""

from django.utils import timezone

from django_transitions.workflow import StateMachineMixin
from django_transitions.workflow import StatusMixin


class LiveStatus(StatusMixin):
    """Workflow for Lifecycle."""

    DEVELOP = 'develop'
    LIVE = 'live'
    MAINTENANCE = 'maintenance'
    DELETED = 'deleted'

    STATE_CHOICES = (
        (DEVELOP, 'Under Development'),
        (LIVE, 'Live'),
        (MAINTENANCE, 'Under Maintenance'),
        (DELETED, 'Deleted'),
    )

    PUBLISH = 'publish'
    MAKE_PRIVATE = 'make_private'
    MARK_DELETED = 'mark_deleted'
    REVERT_DELETED = 'revert_delete'

    TRANSITION_LABELS = {
        PUBLISH : 'Make live',
        MAKE_PRIVATE: 'Under maintenamce',
        MARK_DELETED: 'Mark as deleted',
        REVERT_DELETED: 'Revert Delete',
    }

    SM_STATES = [
        DEVELOP, LIVE, MAINTENANCE, DELETED,
    ]

    SM_INITIAL_STATE = DEVELOP

    SM_TRANSITIONS = [
        # trigger, source, destination
        {
            'trigger': PUBLISH,
            'source': [DEVELOP, MAINTENANCE],
            'dest': LIVE,
        },
        {
            'trigger': MAKE_PRIVATE,
            'source': LIVE,
            'dest': MAINTENANCE,
        },
        {
            'trigger': MARK_DELETED,
            'source': [
                DEVELOP, LIVE, MAINTENANCE,
            ],
            'dest': DELETED,
        },
        {
            'trigger': REVERT_DELETED,
            'source':  DELETED,
            'dest': MAINTENANCE,
        },
    ]


class SiteStateMachineMixin(StateMachineMixin):
    """Lifecycle workflow state machine."""

    status_class = LiveStatus

    machine = Machine(
        model=None,
        finalize_event='wf_finalize',
        auto_transitions=False,
        **status_class.get_kwargs()  # noqa: C815
    )

    @property
    def state(self):
        """Get the items workflowstate or the initial state if none is set."""
        if self.wf_state:
            return self.wf_state
        return self.machine.initial

    @state.setter
    def state(self, value):
        """Set the items workflow state."""
        self.wf_state = value
        return self.wf_state

    def wf_finalize(self, *args, **kwargs):
        """Run this on all transitions."""
        self.wf_date = timezone.now()
