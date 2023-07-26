from django.contrib import admin
from django.urls import path, include

from .views import GoogleLogin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("accounts/", include("allauth.urls")),
    path("dj-rest-auth/google/", GoogleLogin.as_view(), name="google_login"),
]
