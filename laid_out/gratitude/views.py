from logging import getLogger

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404 as drf_get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from laid_out.gratitude.models import GratitudeJournal
from laid_out.gratitude.permissions import IsOwner
from laid_out.gratitude.serializers import GratitudeJournalSerializer

log = getLogger(__name__)


def gratitude_view(request):
    # FIXME: needs pagination
    user_g_journals = None

    try:
        if request.user.is_authenticated:
            queryset = request.user.gratitude_journals.all().order_by("-date_modified")
            if not queryset.exists():
                GratitudeJournal.objects.create(owner=request.user)

            serializer = GratitudeJournalSerializer(queryset, many=True)
            user_g_journals = serializer.data
    except Exception as e:
        log.error(
            "Unexpected error while fetching user gratitude journals"
            f" or creating a gratitude journal for the user: {e}"
        )
        raise

    context = {
        "current_page": "gratitude",
        "user_g_journals": user_g_journals,
        "logged_in": request.user.is_authenticated,
        "GRATITUDE_JOURNAL_API_BASE_URL": reverse("api:gratitude-journals-list"),
    }

    return render(request, "gratitude/home.html", context=context)


class GratitudeJournalViewSet(
    viewsets.GenericViewSet,
):
    serializer_class = GratitudeJournalSerializer
    lookup_field = "g_journal_id"
    lookup_value_regex = r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"

    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return user.gratitude_journals.all()

    def get_user_g_journal_count(self):
        user = self.request.user
        return user.gratitude_journals.count()

    def get_object(self):
        obj = drf_get_object_or_404(self.get_queryset(), pk=self.kwargs["g_journal_id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        try:
            user_g_journal_count = self.get_user_g_journal_count()
            if user_g_journal_count > 150:
                return Response(
                    data={
                        "detail": "You've reached the maximum number of gratitude journals allowed per user. "
                        "This limit is just to fight bots. Please don't hesitate to contact us"
                        " if you'd like to be able to register more gratitude journals!"
                    },
                    status=400,
                )
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return_detail = {"g_journal_id": serializer.data.get("g_journal_id")}

            return Response(data=return_detail, status=201)
        except Exception as e:
            log.error(f"Unexpected error while trying to create gratitude journal: {e}")
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
            log.error(f"Unexpected error while updating gratitude journal: {e}")
            raise

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            log.error(f"Unexpected error while performing gratitude journal update: {e}")
            raise

    def partial_update(self, request, *args, **kwargs):
        try:
            kwargs["partial"] = True
            return self.update(request, *args, **kwargs)
        except Exception as e:
            log.error(f"Unexpected error while partially updating gratitude journal: {e}")
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
            log.error(f"Unexpected error while deleting gratitude journal: {e}")
            raise
