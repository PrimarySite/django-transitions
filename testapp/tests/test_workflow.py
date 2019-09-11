# -*- coding: utf-8 -*-
"""Workflow Tests."""
# Standard Library
import re

# Django
from django.test import TestCase
from django.utils import timezone

# Local
from ..workflows import LiveStatus
from ..models import Lifecycle


class SiteWorkflowTest(TestCase):
    """Test that a user has primarysite elevated Privileges."""

    def setUp(self):  # noqa: D102
        self.lcycle = Lifecycle()

    def test_initial_state(self):
        """Test initial state."""
        assert self.lcycle.state == LiveStatus.DEVELOP

    def test_available_events_initial(self):
        """Test the available events for initial state."""
        events = [e['transition'].name for e in self.lcycle.get_available_events()]
        assert set(events) == {'mark_deleted', 'publish'}

    def test_publish(self):
        """Test the publish transition."""
        dt_before = timezone.now()

        assert self.lcycle.publish()

        dt_after = timezone.now()
        assert self.lcycle.state == LiveStatus.LIVE == self.lcycle.wf_state
        assert dt_before <= self.lcycle.wf_date <= dt_after

    def test_delete_initial(self):
        """Test that delete is possible from initial state."""
        dt_before = timezone.now()

        assert self.lcycle.mark_deleted()

        dt_after = timezone.now()
        assert self.lcycle.state == LiveStatus.DELETED == self.lcycle.wf_state
        assert dt_before <= self.lcycle.wf_date <= dt_after

    def test_graph(self):
        """Compare the graph to ensure the workflow is correct."""
        self.lcycle.save()
        graph = self.lcycle.get_wf_graph()

        assert 'develop -> live' in graph.string()
        assert 'develop -> deleted' in graph.string()
        assert 'live -> deleted' in graph.string()
        assert 'live -> maintenance' in graph.string()
        assert 'deleted -> maintenance' in graph.string()
        assert 'maintenance -> live' in graph.string()
        assert 'maintenance -> deleted' in graph.string()

