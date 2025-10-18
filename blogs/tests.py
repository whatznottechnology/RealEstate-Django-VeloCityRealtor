from django.test import TestCase
from .models import Blog, Tag

class BlogModelTest(TestCase):
    def test_slug_auto_generation(self):
        tag = Tag.objects.create(name="django")
        blog = Blog.objects.create(title="Test Blog Title", content="<p>Test content</p>")
        blog.tags.add(tag)
        self.assertTrue(blog.slug.startswith("test-blog-title"))
        self.assertIn(tag, blog.tags.all())
