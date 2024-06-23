from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *
from .forms import *
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib import messages
from home.forms import MessageForm


class BlogView(View):
    form_message_class = MessageForm
    def get(self, request):

        post_list = Post.objects.all()
        newest_posts = Post.objects.filter().order_by('-created')
        newest_posts = list(reversed(newest_posts))[:5]
    
        paginator = Paginator(post_list, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/blog.html', {"page_obj": page_obj, 
                                                  'message_form':self.form_message_class, 
                                                  'newest_posts':newest_posts})
    
    def post(self, request):
        message_form = self.form_message_class(request.POST)
        
        if request.user.is_authenticated:
        
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.user = request.user
                message.save()
                messages.success(request, 'Your message saved successfully.', 'alert alert-success')
                return redirect('blog:blog')
            
        else:
            return redirect('accounts:login')

        return redirect('blog:blog')



class PostView(View):
    form_class = UserCommentForm
    form_class_reply = UserReplyCommentForm
    form_message_class = MessageForm
    def get(self, request, post_id):
        newest_posts = Post.objects.filter().order_by('-created')
        newest_posts = list(reversed(newest_posts))[:5]

        post = Post.objects.get(id=post_id)
        comments = post.post_comments.filter(is_reply=False)
        
        return render(request, 'blog/blog-detail.html', {'post': post, 'comments':comments, 'form': self.form_class(),
                                                         'message_form':self.form_message_class,
                                                               'form_reply':self.form_class_reply(), 'newest_posts':newest_posts})
        
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        form = self.form_class_reply(request.POST)
        message_form = self.form_message_class(request.POST)
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
        
        if request.user.is_authenticated:
            
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.user = request.user
                message.save()
                messages.success(request, 'Your message saved successfully.', 'alert alert-success')
                return redirect('blog:post', post_id)
            
            else:
                return redirect('home:home')
            
        else:
            return redirect('accounts:login')
            
        


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