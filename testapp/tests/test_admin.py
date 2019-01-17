# -*- coding: utf-8 -*-
"""Admin Tests."""

# Django
from django.test import TestCase
from django.test import RequestFactory
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.admin.sites import AdminSite

# Local
from ..workflows import LiveStatus
from ..admin import LifecycleAdmin
from ..models import Lifecycle

try:
    from unittest import mock
except ImportError:
    import mock


class TestLifecycleAdmin(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.lifecycle = Lifecycle.objects.create()

    @mock.patch('testapp.admin.LifecycleAdmin.message_user')
    def test_response_change(self, mock_message):
        """Trigger a workflow event."""
        data = {'_publish': 'Publish'}
        request = RequestFactory().post('/admin/lifecycle/', data)
        request.user = self.user
        assert self.lifecycle.state == LiveStatus.DEVELOP
        admin_lifecycle = AdminSite()
        before = self.lifecycle.wf_state
        after = LiveStatus.LIVE
        message = 'Status changed from {0} to {1} by transition {2}'.format(
            before, after, 'publish')
        lifecycle_admin = LifecycleAdmin(Lifecycle, admin_lifecycle)

        response = lifecycle_admin.response_change(request, self.lifecycle)

        self.lifecycle.refresh_from_db()
        assert response.status_code == 302
        assert self.lifecycle.state == LiveStatus.LIVE
        mock_message.assert_called_once_with(request, message, messages.SUCCESS)

    @mock.patch('testapp.admin.LifecycleAdmin.message_user')
    def test_response_change_failing_transition(self, mock_message):
        """Trigger a failing workflow event."""
        data = {'_mark_deleted': 'Delete'}
        request = RequestFactory().post('/admin/lifecycle/', data)
        self.lifecycle.mark_deleted = mock.MagicMock()
        self.lifecycle.mark_deleted.return_value = False
        request.user = self.user
        assert self.lifecycle.state == LiveStatus.DEVELOP
        admin_lifecycle = AdminSite()
        before = self.lifecycle.wf_state
        after = LiveStatus.LIVE
        message = 'Status could not be changed from {0} by transition {1}'.format(
            before, 'mark_deleted')
        lifecycle_admin = LifecycleAdmin(Lifecycle, admin_lifecycle)

        response = lifecycle_admin.response_change(request, self.lifecycle)

        self.lifecycle.refresh_from_db()
        assert self.lifecycle.state == LiveStatus.DEVELOP
        mock_message.assert_called_once_with(request, message, messages.ERROR)

    @mock.patch('testapp.admin.LifecycleAdmin.message_user')
    def test_response_change_no_transition(self, mock_message):
        """Trigger a workflow event."""
        data = {'_no_such_transition': 'Publish'}
        request = RequestFactory().post('/admin/lifecycle/', data)
        request.user = self.user
        assert self.lifecycle.state == LiveStatus.DEVELOP
        admin_lifecycle = AdminSite()
        lifecycle_admin = LifecycleAdmin(Lifecycle, admin_lifecycle)
        message = ('The lifecycle '
                   '"<a href="/admin/lifecycle/">{0}</a>" was changed successfully.'.format(
                self.lifecycle))

        response = lifecycle_admin.response_change(request, self.lifecycle)

        self.lifecycle.refresh_from_db()
        assert self.lifecycle.state == LiveStatus.DEVELOP
        mock_message.assert_called_once_with(request, message, messages.SUCCESS)
