from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import jdatetime

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

    def jalali_date(self):
        try:
            local_time = timezone.localtime(self.created_date)
            jd = jdatetime.datetime.fromgregorian(datetime=local_time)
            return jd.strftime('%Y/%m/%d %H:%M')
        except Exception:
            return self.created_date.strftime('%Y-%m-%d %H:%M')

    jalali_date.short_description = 'date (khorshidi) '


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
