from logging import getLogger

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404 as drf_get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from laid_out.goal.models import GoalEntry, demo_goal_data
from laid_out.goal.permissions import IsOwner
from laid_out.goal.serializers import GoalEntrySerializer

log = getLogger(__name__)


def goal_view(request):
    # TODO: needs pagination
    user_goals = None

    try:
        if request.user.is_authenticated:
            queryset = request.user.goal_entries.all().order_by("-date_modified")
            if not queryset.exists():
                GoalEntry.objects.create(owner=request.user, data=demo_goal_data(), name="Tutorial")

            serializer = GoalEntrySerializer(queryset, many=True)
            user_goals = serializer.data
    except Exception as e:
        log.error(f"Unexpected error while fetching user goal or creating a goal for the user: {e}")
        raise

    context = {
        "user_goals": user_goals,
        "logged_in": request.user.is_authenticated,
        "GOAL_API_BASE_URL": reverse("api:goals-list"),
    }

    return render(request, "goal/home.html", context=context)


def error_400_view(request, exception):
    log.warning(
        f"A user hit a 400\n"
        f"request URL: {request.path}\n"
        f"request method: {request.method}"
        f"user: {request.user}\n"
        f"exception: {exception}"
    )
    return render(request, "400.html")


def error_403_view(request, exception):
    log.warning(
        f"A user hit a 403\n"
        f"request URL: {request.path}\n"
        f"request method: {request.method}"
        f"user: {request.user}\n"
        f"exception: {exception}"
    )
    return render(request, "403.html")


def error_404_view(request, exception):
    log.warning(
        f"A user hit a 404\n"
        f"request URL: {request.path}\n"
        f"request method: {request.method}"
        f"user: {request.user}\n"
        f"exception: {exception}"
    )
    return render(request, "404.html")


def error_500_view(request):
    log.error(
        f"We hit a 500\n"
        f"request URL: {request.path}\n"
        f"request method: {request.method}"
        f"user: {request.user}\n"
    )
    return render(request, "500.html")


class GoalEntryViewSet(
    viewsets.GenericViewSet,
):
    serializer_class = GoalEntrySerializer
    lookup_field = "id"
    lookup_value_regex = r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"

    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return user.goal_entries.all()

    def get_goal_entry_count(self):
        user = self.request.user
        return user.goal_entries.count()

    def get_object(self):
        obj = drf_get_object_or_404(self.get_queryset(), pk=self.kwargs["id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        try:
            user_goal_entry_count = self.get_goal_entry_count()
            if user_goal_entry_count > 150:
                return Response(
                    data={
                        "detail": "You've reached the maximum number of goal allowed per user. "
                        "This limit is just to fight bots. Please don't hesitate to contact us"
                        " if you'd like to be able to register more goal!"
                    },
                    status=400,
                )
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return_detail = {"id": serializer.data.get("id")}

            return Response(data=return_detail, status=201)
        except Exception as e:
            log.error(f"Unexpected error while trying to create goal: {e}")
            raise

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, "_prefetched_objects_cache", None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(status=200)

        except Exception as e:
            log.error(f"Unexpected error while updating goal: {e}")
            raise

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            log.error(f"Unexpected error while performing goal update: {e}")
            raise

    def partial_update(self, request, *args, **kwargs):
        try:
            kwargs["partial"] = True
            return self.update(request, *args, **kwargs)
        except Exception as e:
            log.error(f"Unexpected error while partially updating goal: {e}")
            raise

    def destroy(self, request, *args, **kwargs):
        try:
            try:
                instance = self.get_object()
                instance.delete()
            except Http404:
                # this is to handle get_object() gracefully in case the instance doesn't exist
                # the default destroy function from mixins.DestroyModelMixin didn't handle this and returned HTTP 500
                pass

            return Response(status=204)
        except Exception as e:
            log.error(f"Unexpected error while deleting goal: {e}")
            raise
