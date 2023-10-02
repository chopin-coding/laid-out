from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

from django.http import HttpResponse, Http404
from rest_framework import mixins, generics, viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from anxiety.models import AnxietyTree
from anxiety.serializers import AnxietyTreeSerializer


def navbar_helper(
        *,
        request: WSGIRequest,
        current_page: str,
):
    return {
        "current_page": current_page,
        "user_authenticated": request.user.is_authenticated
    }


def index_view(request):
    return render(request, "../templates/index.html", context=navbar_helper(request=request, current_page='home'))


def anxiety_view(request):
    return render(request, "anxiety/anxiety.html", context=navbar_helper(request=request, current_page='anxiety'))


def htmx_test_view(request):
    return HttpResponse("HTMX test")


def account_view(request):
    return render(request, "account.html", context=navbar_helper(request=request, current_page='account_details'))


def about_view(request):
    return render(request, "about.html", context=navbar_helper(request=request, current_page='about'))


class AnxietyTreeViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = AnxietyTree.objects.all()
    serializer_class = AnxietyTreeSerializer
    lookup_field = "tree_id"
    lookup_value_regex = (
        r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
    )

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(pk=self.kwargs["tree_id"])
        return obj

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
        try:
            instance = self.get_object()
            instance.delete()
        except ObjectDoesNotExist:
            # this is to handle get_object() gracefully in case the instance doesn't exist
            # the default destroy function from mixins.DestroyModelMixin didn't handle this and returned HTTP 500
            pass

        return Response(status=204)
