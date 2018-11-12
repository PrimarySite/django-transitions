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


def compare_no_whitespace(a, b):
    """Compare two base strings, disregarding whitespace."""
    return re.sub('\s*"*', '', a) == re.sub('\s*"*', '', b)


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
        site_wf_graph = """
            digraph "" {
                graph [compound=True,
                    label="Lifecycle",
                    rankdir=LR,
                    ratio=0.3
                ];
                node [color=black,
                    fillcolor=white,
                    height=1.2,
                    shape=circle,
                    style=filled
                ];
                edge [color=black];
                develop  [color=red,
                    fillcolor=darksalmon,
                    shape=doublecircle];
                develop -> live  [label=publish];
                develop -> deleted   [label=mark_deleted];
                live -> deleted  [label=mark_deleted];
                live -> maintenance  [label=make_private];
                deleted -> maintenance   [label=revert_delete];
                maintenance -> live  [label=publish];
                maintenance -> deleted   [label=mark_deleted];
            }
        """
        graph = self.lcycle.get_wf_graph()

        assert compare_no_whitespace(graph.string(), site_wf_graph)
