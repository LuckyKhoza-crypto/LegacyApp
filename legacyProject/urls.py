"""
URL configuration for todo_project project
"""
from django.contrib import admin
from django.urls import path, include,  re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('legacyApp.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path("__reload__/", include("django_browser_reload.urls")),

    #authentication urls
    # path('', TemplateView.as_view(template_name='index.html')),
    path('accounts/', include('allauth.urls')), # all OAuth operations will be performed under this route
    # path('logout', LogoutView.as_view())  default Django logout view at / logout,

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
