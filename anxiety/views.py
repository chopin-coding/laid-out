from django.shortcuts import render

from django.http import HttpResponse, Http404
from rest_framework import mixins, generics, viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from anxiety.models import AnxietyTree
from anxiety.serializers import AnxietyTreeSerializer


def index_view(request):
    return render(request, "../templates/index.html")


def anxiety_view(request):
    anxiety_list = 123

    return render(request, "anxiety/anxiety.html", {"anxiety_list": anxiety_list})


def htmx_test_view(request):
    return HttpResponse("HTMX test")


class AnxietyTreeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    queryset = AnxietyTree.objects.all()
    serializer_class = AnxietyTreeSerializer
    lookup_field = 'tree_id'
    lookup_value_regex = '[0-9a-f]{32}'

    def get_queryset(self):
        queryset = AnxietyTree.objects.all()
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.get(pk=self.kwargs['pk'])
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return_string = {"tree_id": serializer.data.get("tree_id")}
        return Response(return_string, status=201)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(status=200)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)



