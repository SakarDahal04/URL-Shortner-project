from django.urls import path
from shorten_url.views import (
    ShortenUrlCreateAPIView,
    ShortUrlRedirectAPIView,
    ShortUrlListAPIView,
    ShortUrlRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("shorten/", ShortenUrlCreateAPIView.as_view(), name="shorten_url"),
    path("url_list/", ShortUrlListAPIView.as_view(), name="list_urls"),
    path(
        "redirect/<str:short_code>/",
        ShortUrlRedirectAPIView.as_view(),
        name="short-url-redirect",
    ),
    path(
        "<str:short_url_id>/",
        ShortUrlRetrieveUpdateDestroyAPIView.as_view(),
        name="url-update-delete-receive",
    ),
]
