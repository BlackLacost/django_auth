import functools

from django.http import HttpResponse
from django.shortcuts import redirect


def anonymous_required(func=None, authenticated_redirect_url="home"):
    if func is None:
        return functools.partial(
            anonymous_required,
            authenticated_redirect_url=authenticated_redirect_url,
        )

    @functools.wraps(func)
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(authenticated_redirect_url)
        return func(request, *args, **kwargs)

    return inner


def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(
                    "You are not authorized to view this page"
                )

        return wrapper_func

    return decorator


def stuff_only(view_func):
    @functools.wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "customer":
            return redirect("home")

        if group == "stuff":
            return view_func(request, *args, **kwargs)

    return wrapper_func
