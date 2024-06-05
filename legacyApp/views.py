from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Event
from .models import Comment as CommentModel

from .forms import CommentForm
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse


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
