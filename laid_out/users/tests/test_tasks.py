import pytest
from celery.result import EagerResult

from laid_out.users.models import User
from laid_out.users.tasks import delete_all_inactive_users, delete_user_task

pytestmark = pytest.mark.django_db


class TestDeleteUserTask:
    def test_happy_path(self, user: User, settings):
        settings.CELERY_TASK_ALWAYS_EAGER = True
        task_result = delete_user_task.delay(username=user.username)

        # the user is deleted
        assert isinstance(task_result, EagerResult)
        with pytest.raises(User.DoesNotExist):
            User.objects.get(username=user.username)


class TestDeleteAllInactiveUsersTask:
    def test_inactive_users_exist(self, user: User, settings):
        settings.CELERY_TASK_ALWAYS_EAGER = True
        user.is_active = False
        user.save()

        task_result = delete_all_inactive_users.delay()

        # the user is deleted
        assert isinstance(task_result, EagerResult)
        with pytest.raises(User.DoesNotExist):
            User.objects.get(username=user.username)

    def test_no_inactive_users_exist(self, user: User, settings):
        settings.CELERY_TASK_ALWAYS_EAGER = True

        task_result = delete_all_inactive_users.delay()

        # the user is not deleted
        assert isinstance(task_result, EagerResult)
        assert User.objects.get(username=user.username) == user
