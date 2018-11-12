# -*- coding: utf-8 -*-
"""Mixins for transition workflows."""

# Standard Library
from functools import partial

# 3rd-party
from transitions.extensions import MachineFactory


class StatusBase(object):
    """Base class for transitions and status definitions."""

    STATE_CHOICES = (
        # Override this!
        # https://docs.djangoproject.com/en/2.1/ref/models/fields/#choices
        # to provide human readable labels for states
        # (state, 'My Workflow state'),
    )

    TRANSITION_LABELS = {
        # Override this!
        # Provide human readable labels for transitions
        # transition: 'Label',
    }

    SM_STATES = [
        # Override this!
        # list of available workflow states
    ]

    SM_INITIAL_STATE = None  # Initial state of the machine. Override this!

    SM_TRANSITIONS = [
        # Override this!
        # trigger, source, destination
    ]

    @classmethod
    def get_kwargs(cls):
        """Get the kwargs to initialize the state machine."""
        kwargs = {
            'initial': cls.SM_INITIAL_STATE,
            'states': cls.SM_STATES,
            'transitions': cls.SM_TRANSITIONS,
        }
        return kwargs


class StateMachineMixinBase(object):
    """
    Base class for state machine mixins.

    * `status_class` must provide TRANSITION_LABELS
      and the get_kwargs class method (see StatusBase).
    * `machine` is a transition machine

    e.g::

        machine = Machine(
            model=None,
            finalize_event='wf_finalize',
            auto_transitions=False,
            **status_class.get_kwargs()  # noqa: C815
        )

    """

    status_class = None  # Override this!
    machine = None  # Override this!

    @property
    def state(self):  # pragma: no cover
        """
        Get the items workflowstate or the initial state if none is set.

        E.g::

            if self.wf_state:
                return self.wf_state
            return self.machine.initial

        """
        raise NotImplementedError('To be implemented in subclass')

    @state.setter
    def state(self, value):  # pragma: no cover
        """
        Set the items workflow state.

        E.g::

            self.wf_state = value
            return self.wf_state

        """
        raise NotImplementedError('To be implemented in subclass')

    def get_available_events(self):
        """
        Get available workflow transition events for the current state.

        Returns a dictionary:
            * 'transition': transition event.
            * 'label': human readable label for the event
        """
        for trigger in self.machine.get_triggers(self.state):
            event = self.machine.events[trigger]
            yield {
                   'transition': event,
                   'label': self.status_class.TRANSITION_LABELS[event.name],
            }

    def get_wf_graph(self):
        """Get the graph for this machine."""
        diagram_cls = MachineFactory.get_predefined(graph=True)
        machine = diagram_cls(
            model=self,
            auto_transitions=False,
            title=type(self).__name__,
            **self.status_class.get_kwargs()  # noqa: C815
        )
        return machine.get_graph()

    def __getattribute__(self, item):
        """Propagate events to the workflow state machine."""
        try:
            return super(StateMachineMixinBase, self).__getattribute__(item)
        except AttributeError:
            if item in self.machine.events:
                return partial(self.machine.events[item].trigger, self)
            raise
