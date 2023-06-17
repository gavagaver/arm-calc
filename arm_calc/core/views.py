from django.shortcuts import render


def page_not_found(request, exception):
    """
    Renders a 404 error page with the path of the requested URL.
    """
    return render(
        request,
        template_name='core/404.html',
        context={'path': request.path},
        status=404,
    )


def csrf_failure(request, reason=''):
    """
    Renders a 403 error page for CSRF failures.
    """
    return render(
        request,
        template_name='core/403csrf.html',
    )


def server_error(request):
    """
    Renders a 500 error page for server errors.
    """
    return render(
        request,
        template_name='core/500.html',
        status=500,
    )


def permission_denied(request, exception):
    """
    Renders a 403 error page for permission denied errors.
    """
    return render(
        request,
        template_name='core/403.html',
        status=403,
    )
