from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from laid_out.anxiety.views import log
from laid_out.users.models import User
from laid_out.users.tasks import delete_user_task


def user_detail_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse("account_login"))

    context = {
        "current_page": "user_detail",
    }

    return render(request, "users/detail.html", context=context)


def user_delete_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse("account_login"))
    elif request.method == "POST":
        try:
            user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            log.error("The user trying to be deleted does not exist")
            return redirect(reverse("home"))
        except Exception as e:
            log.error(f"Unexpected error while fetching user to delete: {e}")
            messages.error(request, "Unexpected error. Please try again.")
            return redirect(reverse("home"))

        if user:
            try:
                user.is_active = False
                user.save()

                delete_user_task.delay(user_name=user.username)
                messages.success(
                    request,
                    "Your account has been marked for deletion and will be deleted within 24 hours.",
                )
            except Exception as e:
                log.error(f"Unexpected error in {__name__}: {e}")
                messages.error(
                    request,
                    "Problem deleting account. Please try again or contact the administrator.",
                )

            finally:
                return redirect(reverse("home"))

    context = {
        "current_page": "user_delete",
    }

    return render(request, "users/delete.html", context=context)
