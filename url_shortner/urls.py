from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account import views

urlpatterns = [
    path('', views.index, name='home'),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),

    path('url/', include("shorten_url.urls")),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
