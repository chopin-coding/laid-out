from django.shortcuts import render

from django.http import HttpResponse, Http404
from rest_framework import mixins, generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from anxiety.models import AnxietyTree
from anxiety.serializers import AnxietyTreeSerializer


def index_view(request):
    return render(request, "../templates/index.html")


def anxiety_view(request):
    anxiety_list = 123

    return render(request, "anxiety/anxiety.html", {"anxiety_list": anxiety_list})


def htmx_test_view(request):
    return HttpResponse("HTMX test")


class AnxietyTreeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = AnxietyTree.objects.all()
    serializer_class = AnxietyTreeSerializer
