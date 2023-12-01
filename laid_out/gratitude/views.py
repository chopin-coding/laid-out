from logging import getLogger

from django.shortcuts import render

# Create your views here.

log = getLogger(__name__)


def gratitude_view(request):
    context = {
        "current_page": "gratitude",
        "logged_in": request.user.is_authenticated,
    }

    return render(request, "gratitude/home.html", context=context)
