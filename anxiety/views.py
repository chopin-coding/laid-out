from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from django.http import HttpResponse, Http404
from django.urls import reverse
from rest_framework import mixins, generics, viewsets, permissions
from rest_framework.exceptions import ValidationError
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
    if request.user.is_authenticated:
        # queryset = AnxietyTree.objects.filter(owner=request.user)
        queryset = request.user.anxiety_trees.all()
        if not queryset.exists():
            AnxietyTree.objects.create(owner=request.user)

        serializer = AnxietyTreeSerializer(queryset, many=True)
        serialized_user_trees = serializer.data

    context = {
        "current_page": "anxiety",
        "user_trees": serialized_user_trees,
        "logged_in": request.user.is_authenticated,
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
        "current_page": "account_about",
    }

    return render(request, "about.html", context=context)


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

    def get_object(self):
        # queryset = self.get_queryset()
        # obj = queryset.get(pk=self.kwargs["tree_id"])
        # return obj

        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return_string = {"tree_id": serializer.data.get("tree_id")}
        return Response(return_string, status=201)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(status=200)

    def destroy(self, request, *args, **kwargs):
        # try:
        #     instance = self.get_object()
        #     instance.delete()
        # except ObjectDoesNotExist:
        #     # this is to handle get_object() gracefully in case the instance doesn't exist
        #     # the default destroy function from mixins.DestroyModelMixin didn't handle this and returned HTTP 500
        #     pass
        #
        # return Response(status=204)

        instance = self.get_object()
        instance.delete()
        return Response(status=204)
