from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    img = models.FileField(upload_to='images', default=None, blank=True, null=True)
    body = models.TextField()
    img2 = models.FileField(upload_to='images', default=None, blank=True, null=True)
    body2 = models.TextField(default=None, blank=True, null=True)
    img3 = models.FileField(upload_to='images', default=None, blank=True, null=True)
    body2 = models.TextField(default=None, blank=True, null=True)
    audio = models.FileField(upload_to='images', default=None, blank=True, null=True)
    video = models.FileField(upload_to='images', default=None, blank=True, null=True)
    writer = models.CharField(max_length=100, default=None)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.slug} - {self.created}'
    
    def get_absolute_url(self):
        return reverse("blog:post", args=(self.id, self.slug))
    
    def like_counter(self):
        return self.post_votes.count()
    
    def comment_counter(self):
        return self.post_comments.count()
    
    

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post_votes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_votes')
    
    def __str__(self):
        return f'{self.user} liked {self.post}' 
    
    
class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', default=None, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    body = models.TextField(max_length=300)
    name = models.CharField(max_length=100, default='anonymous', blank=True, null=True)
    email = models.EmailField(default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_reply = models.BooleanField(default=False)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='comment_replies', blank=True, null=True)
    
    def __str__(self):
        return f'{self.user} - {self.body[:20]}'
    
    
class Subscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

