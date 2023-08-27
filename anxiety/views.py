from django.shortcuts import render

from django.http import HttpResponse


def index_view(request):
    return render(request, "anxiety/index.html")


def anxiety_view(request):
    anxiety_list = 123

    return render(request, "anxiety/anxiety.html", {"anxiety_list": anxiety_list})


def htmx_test_view(request):
    return HttpResponse("HTMX test")
