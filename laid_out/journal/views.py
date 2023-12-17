from logging import getLogger

from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404 as drf_get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from laid_out.journal.models import Journal
from laid_out.journal.permissions import IsOwner
from laid_out.journal.serializers import JournalSerializer

log = getLogger(__name__)


def journal_view(request):
    # FIXME: needs pagination
    user_journals = None

    try:
        if request.user.is_authenticated:
            queryset = request.user.journals.all().order_by("-date_modified")
            if not queryset.exists():
                Journal.objects.create(owner=request.user)

            serializer = JournalSerializer(queryset, many=True)
            user_journals = serializer.data
    except Exception as e:
        log.error("Unexpected error while fetching user journals" f" or creating a journal for the user: {e}")
        raise

    context = {
        "current_page": "journal",
        "user_journals": user_journals,
        "logged_in": request.user.is_authenticated,
        "JOURNAL_API_BASE_URL": "http://localhost:8000/api/journals/",  # FIXME
    }

    return render(request, "journal/home.html", context=context)


class JournalViewSet(
    viewsets.GenericViewSet,
):
    serializer_class = JournalSerializer
    lookup_field = "journal_id"
    lookup_value_regex = r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"

    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return user.journals.all()

    def get_user_journal_count(self):
        user = self.request.user
        return user.journals.count()

    def get_object(self):
        obj = drf_get_object_or_404(self.get_queryset(), pk=self.kwargs["journal_id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        try:
            user_journal_count = self.get_user_journal_count()
            if user_journal_count > 150:
                return Response(
                    data={
                        "detail": "You've reached the maximum number of journals allowed per user. "
                        "This limit is just to fight bots. Please don't hesitate to contact me"
                        " if you'd like to be able to register more journals at once!"
                    },
                    status=400,
                )
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return_detail = {"journal_id": serializer.data.get("journal_id")}

            return Response(data=return_detail, status=201)
        except Exception as e:
            log.error(f"Unexpected error while trying to create journal: {e}")
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
            log.error(f"Unexpected error while updating journal: {e}")
            raise

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            log.error(f"Unexpected error while performing journal update: {e}")
            raise

    def partial_update(self, request, *args, **kwargs):
        try:
            kwargs["partial"] = True
            return self.update(request, *args, **kwargs)
        except Exception as e:
            log.error(f"Unexpected error while partially updating journal: {e}")
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
            log.error(f"Unexpected error while deleting journal: {e}")
            raise
