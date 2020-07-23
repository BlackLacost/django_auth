from braces.views import AnonymousRequiredMixin
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .decorators import allowed_users, anonymous_required, stuff_only


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def home_view(request):
    return render(request, "home.html")


@login_required(login_url="login")
@stuff_only
def stuff_view(request):
    return render(request, "stuff.html")


@anonymous_required
def signup_view(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="customer")
            user.groups.add(group)
            messages.success(
                request, f"Account was created for {user.username}"
            )

            return redirect("login")
    return render(request, "account/signup.html", {"form": form})


class LoginView(AnonymousRequiredMixin, auth_views.LoginView):
    authenticated_redirect_url = reverse_lazy("stuff")
    redirect_field_name = reverse_lazy("stuff")
    template_name = "account/login.html"


login_view = LoginView.as_view()


def logout_view(request):
    logout(request)
    return redirect("login")
