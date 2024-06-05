from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.BlogListView.as_view(), name='blog'),
    path('post_details/<int:pk>',
         views.PostDetailsView.as_view(), name='post_details'),
    path('post_details/<int:pk>/',
         views.CreateCommentView.as_view(), name='comments'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
