from django.test import TestCase
from .models import Post, Event, Comment
# Create your tests here.


class PostTest(TestCase):

    def test_post_model_exists(self):
        post = Post.objects.count()

        self.assertEqual(post, 0)
