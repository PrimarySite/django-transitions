# -*- coding: utf-8 -*-
"""Example Lifecycle workflow."""

from django.utils import timezone

from django_transitions.workflow import StateMachineMixinBase
from django_transitions.workflow import StatusBase

from transitions import Machine


class LiveStatus(StatusBase):
    """Workflow for Lifecycle."""

    # Define the states as constants
    DEVELOP = 'develop'
    LIVE = 'live'
    MAINTENANCE = 'maintenance'
    DELETED = 'deleted'

    # Give the states a human readable label
    STATE_CHOICES = (
        (DEVELOP, 'Under Development'),
        (LIVE, 'Live'),
        (MAINTENANCE, 'Under Maintenance'),
        (DELETED, 'Deleted'),
    )

    # Define the transitions as constants
    PUBLISH = 'publish'
    MAKE_PRIVATE = 'make_private'
    MARK_DELETED = 'mark_deleted'
    REVERT_DELETED = 'revert_delete'

    # Give the transitions a human readable label
    # which will be used in the django admin
    TRANSITION_LABELS = {
        PUBLISH : 'Make live',
        MAKE_PRIVATE: 'Under maintenamce',
        MARK_DELETED: 'Mark as deleted',
        REVERT_DELETED: 'Revert Delete',
    }

    # Construct the values to pass to the state machine constructor

    # The states of the machine
    SM_STATES = [
        DEVELOP, LIVE, MAINTENANCE, DELETED,
    ]

    # The machines initial state
    SM_INITIAL_STATE = DEVELOP

    # The transititions as a list of dictionaries
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


class LifecycleStateMachineMixin(StateMachineMixinBase):
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
