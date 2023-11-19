from logging import getLogger
from time import sleep

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404, HttpResponse, HttpResponseServerError
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from rest_framework import viewsets
from rest_framework.generics import get_object_or_404 as drf_get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from anxiety.models import AnxietyTree
from anxiety.permissions import IsOwner
from anxiety.serializers import AnxietyTreeSerializer
from anxiety.tasks import send_feedback_email_task

log = getLogger(__name__)


def index_view(request):
    context = {
        "current_page": "home",
    }

    return render(request, "../templates/index.html", context=context)


def anxiety_view(request):
    # FIXME: This view for a user with a large number of large-sized trees could slow the whole
    #  app down since this is not async
    user_trees = None

    try:
        if request.user.is_authenticated:
            queryset = request.user.anxiety_trees.all().order_by('-date_modified')
            if not queryset.exists():
                AnxietyTree.objects.create(owner=request.user)

            serializer = AnxietyTreeSerializer(queryset, many=True)
            user_trees = serializer.data
    except Exception as e:
        log.error(f"Unexpected error while fetching user trees or creating a tree for the user: {e}")

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
    messages.success(request, 'The quick brown fox jumps over the lazy dog. '
                              'The quick brown fox jumps over the lazy dog. ')  # TODO: remove before prod
    messages.warning(request, 'The quick brown fox jumps over the lazy dog. '
                              'The quick brown fox jumps over the lazy dog. ')  # TODO: remove before prod
    messages.error(request, 'second toast')  # TODO: remove before prod
    messages.info(request, 'second toast')  # TODO: remove before prod

    if request.user.is_authenticated:
        send_feedback_email_task.delay(email_address=request.user.email, message="asd")


    return render(request, "about.html", context=context)


def account_delete_view(request):
    if not request.user.is_authenticated:

        return redirect(reverse("account_login"))
    elif request.method == 'POST':
        # TODO: maybe set the account inactive instead of deleting it?

        try:
            user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            print("The user trying to be deleted does not exist")
            return redirect(reverse("index"))
        except Exception as e:
            print(f"Unexpected error while fetching user to delete: {e}")
            messages.error(request, "Unexpected error. Please try again.")
            return redirect(reverse("index"))

        if user:
            try:
                user.delete()
                messages.success(request, "Your account has been deleted.")
                return redirect(reverse("index"))
            except Exception as e:
                print(f"Unexpected error while deleting user: {e}")
                messages.error(request,
                               "Error while trying to delete user. Please try again or contact the administrator.")
                return redirect(reverse("index"))

    context = {
        "current_page": "account_delete",
    }

    return render(request, "account/delete.html", context=context)


def error_404_view(request, exception):
    log.warning(
        f"A user hit a 404\n"
        f"request URL: {request.path}\n"
        f"request method: {request.method}"
        f"user: {request.user}\n"
        f"exception: {exception}"
    )
    return render(request, 'base/404.html')


def error_500_view(request):
    log.error(
        f"We hit a 500\n"
        f"request URL: {request.path}\n"
        f"request method: {request.method}"
        f"user: {request.user}\n"
    )
    return render(request, 'base/500.html')


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
        obj = drf_get_object_or_404(self.get_queryset(), pk=self.kwargs["tree_id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        try:
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
        except Exception as e:
            log.error(f"Unexpected error while trying to create tree: {e}")

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

        #  TODO: handle more specific exceptions?
        except Exception as e:
            log.error(f"Unexpected error while updating tree: {e}")

    def perform_update(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            log.error(f"Unexpected error while performing tree update: {e}")

    def partial_update(self, request, *args, **kwargs):
        try:
            kwargs["partial"] = True
            return self.update(request, *args, **kwargs)
        except Exception as e:
            log.error(f"Unexpected error while partially updating tree: {e}")

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
            log.error(f"Unexpected error while deleting tree: {e}")
