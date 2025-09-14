from django.utils.decorators import decorator_from_middleware
from django.middleware.cache import CacheMiddleware


class RevalidateBackHistoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Add headers to revalidate back history
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = 'Fri, 01 Jan 1990 00:00:00 GMT'

        return response


# Decorator to apply the middleware to views
revalidate_back_history = decorator_from_middleware(RevalidateBackHistoryMiddleware)

from django.shortcuts import redirect
from django.http import HttpResponseNotFound

from django.shortcuts import render, redirect
from django.urls import reverse


class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            # Option 1: Redirect to login
            # return redirect('/backend/login/')
            return redirect(reverse('backend/dashboard'))  # or the appropriate URL for the dashboard

            # Option 2: Render custom page
            # return render(request, '404.html', status=404)

        return response

