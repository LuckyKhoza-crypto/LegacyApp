import os
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Event
from .models import Comment as CommentModel
from . import models

from .forms import CommentForm
from django.views.decorators.http import require_http_methods

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse

# authentication imports

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from . import models


def sign_in(request):
    return render(request, 'sign_in.html')


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

    # In a real app, I'd also save any new user here to the database. See below for a real example I wrote for Photon Designer.
    # You could also authenticate the user here using the details from Google (https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-in)
    request.session['user_data'] = user_data

    return redirect('blog')


def sign_out(request):
    del request.session['user_data']
    return redirect('sign_in')


@method_decorator(csrf_exempt, name='dispatch')
class AuthGoogle(APIView):
    """
    Google calls this URL after the user has signed in with their Google account.
    """

    def post(self, request, *args, **kwargs):
        try:
            user_data = self.get_google_user_data(request)
        except ValueError:
            return HttpResponse("Invalid Google token", status=403)

        email = user_data["email"]
        user, created = models.User.objects.get_or_create(
            email=email, defaults={
                "username": email, "sign_up_method": "google",
                "first_name": user_data.get("given_name"),
            }
        )

        # Add any other logic, such as setting a http only auth cookie as needed here.
        return HttpResponse(status=200)

    @staticmethod
    def get_google_user_data(request: HttpRequest):
        token = request.POST['credential']
        return id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )


class BlogListView(ListView):

    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'  # name of the object that will be used in the template
    ordering = '-created_date'  # ordering the posts by date_posted


class PostDetailsView(DetailView):
    model = Post  # the used model
    template_name = 'post_details.html'

    def get_context_data(self, **kwargs):
        # add the form and the comments to the context
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = CommentModel.objects.filter(
            post=self.kwargs['pk'])
        context['events'] = Event.objects.filter(post=self.kwargs['pk'])

        return context


class CreateCommentView(CreateView):
    model = CommentModel
    form_class = CommentForm
    template_name = 'post_details.html'

    def form_valid(self, form):
        # Associate comment with post
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        form.save()  # Save the form data to the database

        if self.request.headers.get('HX-Request'):
            return self.render_to_response_htmx()  # Return the response as HTMX
        else:
            return super().form_valid(form)

    def render_to_response_htmx(self):
        comments = CommentModel.objects.filter(
            post=self.kwargs['pk'])  # Get the comments for the post
        return render(self.request, 'partials/comments_list.html', {'comments': comments})

    def get_success_url(self):
        # Redirect to the post details page after comment is created
        return reverse('post_details', kwargs={'pk': self.kwargs['pk']})
