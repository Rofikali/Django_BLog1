from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model


from django.conf import settings

# u = settings.AUTH_USER_MODEL

# print()
# print('U only ', u)


User = get_user_model()

# print()
# print('User only', User)


class Posts(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    slug = models.SlugField(
        unique=True, allow_unicode=True, blank=True, null=True)
    image = models.ImageField(
        upload_to='images/', height_field='height_field', width_field='width_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_user', default=1)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = ("Post")
        verbose_name_plural = ("Posts")
        ordering = ['-timestamp', '-updated']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs={'id': self.pk})
