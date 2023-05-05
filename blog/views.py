from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *
from .forms import *
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib import messages


class BlogView(View):
    def get(self, request):

        post_list = Post.objects.all()
        newest_posts = Post.objects.filter().order_by('-created')
        newest_posts = list(reversed(newest_posts))[:5]
    
        paginator = Paginator(post_list, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/blog.html', {"page_obj": page_obj, 'newest_posts':newest_posts})
    
    def post(self, request):
        email = request.POST['sub-email']
        user = request.user
        if user.is_authenticated:
            subscriber = Subscribe.objects.filter(email=email).exists()
            if subscriber:
                messages.warning(request, 'this email is already subscribed !', 'alert alert-warning')
            else:
                Subscribe.objects.create(user=user, email=email)
                messages.success(request, 'You are Subscribed !', 'alert alert-success')
            
        else:
            return redirect('accounts:login')
            
        return redirect('blog:blog')



class PostView(View):
    form_class = UserCommentForm
    form_class_reply = UserReplyCommentForm
    def get(self, request, post_id):
        newest_posts = Post.objects.filter().order_by('-created')
        newest_posts = list(reversed(newest_posts))[:5]
        
        post = Post.objects.get(id=post_id)
        comments = post.post_comments.filter(is_reply=False)
        
        return render(request, 'blog/blog-detail.html', {'post': post, 'comments':comments, 'form': self.form_class(),
                                                               'form_reply':self.form_class_reply(), 'newest_posts':newest_posts})
        
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        form = self.form_class_reply(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            if request.user.is_authenticated:
                new_comment.user = request.user
                if new_comment.name == 'anonymous':
                    new_comment.name = request.user.username
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'your comment was sent successfuly !', 'alert alert-success')
            return redirect('blog:post', new_comment.post.id)
        
        
class CommentReplyView(View):
    form_class_reply = UserReplyCommentForm
    
    def post(self, request, post_id, comment_id):
        form = self.form_class_reply(request.POST)
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(PostComment, id=comment_id)
        if form.is_valid():
            reply = form.save(commit=False)
            if request.user.is_authenticated:
                reply.user = request.user
                if reply.name == 'anonymous':
                    reply.name = request.user.username
            reply.post = post
            reply.is_reply = True
            reply.reply =comment
            reply.save()
            
            messages.success(request, 'your commnet was sent successfuly !', 'alert alert-success')
        return redirect('blog:post', post.id)