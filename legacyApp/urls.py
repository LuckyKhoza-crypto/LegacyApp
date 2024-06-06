from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('1', views.BlogListView.as_view(), name='blog'),
    path('post_details/<int:pk>',
         views.PostDetailsView.as_view(), name='post_details'),
    path('post_details/<int:pk>/',
         views.CreateCommentView.as_view(), name='comments'),
         
    path('', views.sign_in, name='sign_in'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
