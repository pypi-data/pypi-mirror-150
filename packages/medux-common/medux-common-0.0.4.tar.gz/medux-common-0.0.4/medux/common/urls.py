from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

# namespaced URLs
app_name = "common"

# URLs namespaced  under common/
urlpatterns = [
    # path("", views.IndexView.as_view(), name="index"),
]


# global URLs
root_urlpatterns = [
    # path("api/foo", views.APIView.as_view(), name="api"),
]


# URLpatterns that should be part of all plugins and hosts and can
# be used there.
common_urlpatterns = [
    path(
        "accounts/login/",
        LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        LogoutView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
]

if settings.DEBUG:
    common_urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
