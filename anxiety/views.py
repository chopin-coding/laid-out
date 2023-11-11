from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from anxiety.models import AnxietyTree
from anxiety.permissions import IsOwner
from anxiety.serializers import AnxietyTreeSerializer


def index_view(request):
    context = {
        "current_page": "home",
    }

    return render(request, "../templates/index.html", context=context)


def anxiety_view(request):
    # FIXME: This view for a user with a large number of large-sized trees could slow the whole
    #  app down since this is not async

    if request.user.is_authenticated:
        queryset = request.user.anxiety_trees.all().order_by('-date_modified')
        if not queryset.exists():
            AnxietyTree.objects.create(owner=request.user)

        serializer = AnxietyTreeSerializer(queryset, many=True)
        user_trees = serializer.data
    else:
        user_trees = None

    context = {
        "current_page": "anxiety",
        "user_trees": user_trees,
        "logged_in": request.user.is_authenticated,
        "ANXIETY_API_BASE_URL": "http://127.0.0.1:8000/anxiety/api/trees/"  # FIXME
    }

    return render(request, "anxiety/anxiety.html", context=context)


def htmx_test_view(request):
    return HttpResponse("HTMX test")


def account_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse("account_login"))

    context = {
        "current_page": "account_details",
    }

    return render(request, "account.html", context=context)


def about_view(request):
    context = {
        "current_page": "about",
    }
    messages.success(request, 'please be in the center')  # TODO: remove before prod

    return render(request, "about.html", context=context)


def error_404_view(request, exception):
    return render(request, 'base/404.html')


class AnxietyTreeViewSet(
    viewsets.GenericViewSet,
):
    serializer_class = AnxietyTreeSerializer
    lookup_field = "tree_id"
    lookup_value_regex = (
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
    )

    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return user.anxiety_trees.all()

    def get_user_tree_count(self):
        user = self.request.user
        return user.anxiety_trees.count()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["tree_id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user_tree_count = self.get_user_tree_count()
        if user_tree_count > 150:
            return Response(
                data={"detail": f"You've reached the maximum number of trees allowed per user. "
                                f"This limit is just to fight bots. Please don't hesitate to contact me if you'd "
                                f"like to be able to register more trees!"},
                status=400)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return_detail = {"tree_id": serializer.data.get("tree_id")}

        return Response(data=return_detail, status=201)

    def update(self, request, *args, **kwargs):
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

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
        except Http404:
            # this is to handle get_object() gracefully in case the instance doesn't exist
            # the default destroy function from mixins.DestroyModelMixin didn't handle this and returned HTTP 500
            pass

        return Response(status=204)
