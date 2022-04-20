from django import template
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, 
        CreateView, 
        View,
        UpdateView,
        DeleteView,)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (LoginRequiredMixin, 
        UserPassesTestMixin)
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Subforum, Category, Post, Thread
from .forms import ThreadForm, PostForm


class HomeView(ListView):
    # shows a categories and subfora with description

    # get all subforum
    queryset = Subforum.objects.all()
    template_name = 'home.html'

    def get_context_data(self, **kwargs):

        categories = Category.objects.all()
        context = {}
        forum_layout = {}

        for category in categories:
            forum_layout[category.name] = []

        # assign all subforum to the right category (specified by admin)
        for subforum in self.queryset:
            forum_layout[str(subforum.category)].append(subforum)
        context['layout'] = forum_layout

        return context

class SubforumView(ListView):
    # presents all threads in a subforum

    template_name = 'subforum.html'

    def get_queryset(self):
        return Subforum.objects.get(path=self.kwargs['subforum'])

    def get_context_data(self, **kwargs):

        path = self.kwargs['subforum']
        curr_subforum = Subforum.objects.get(path=path)
        # in the future we set subforum to the entire object
        context = { 'subforum': curr_subforum }
        queryset = Thread.objects.filter(subforum__path=path)
        context['thread_list'] = queryset
        return context

class ThreadView(View):

    template_name = 'thread.html'
    form = PostForm()

    def get_replies(self, reply_context, post, depth=1):
        replies = Post.objects.filter(repliesTo=post.id)
        if replies:
            reply_context[post.id] = (depth, replies)
            for reply in replies:
                self.get_replies(reply_context, reply, depth+1)

    def get(self, request, *args, **kwargs):
        context = {}
        thread = Thread.objects.get(slug=kwargs['slug'])
        posts = Post.objects.filter(thread__id=thread.id)
        context['form'] = self.form
        context['thread'] = thread
        context['posts'] = posts

        reply_context = {}
        for post in posts:
            self.get_replies(reply_context, post)
        # pairs are (depth, reply_queryset) pairs
        context['pairs'] = reply_context

        t = template.loader.get_template(self.template_name)
        return HttpResponse(t.render(context, request=request))

    def post(self, request, *args, **kwargs):
        '''
        We differentiate posts and replies even though they are
        both instances of Post
        '''
        author = User.objects.get(username=request.user)

        if 'thread_reply' in request.POST:
            threadReplied = Thread.objects.get(
                    id=request.POST['thread_reply'])

            post = Post(body = request.POST['body'],
                    author = author,
                    thread = threadReplied)
            post.save()

        elif 'post_reply' in request.POST:
            postReplied = Post.objects.get(id=request.POST['post_reply'])
            reply = Post(body = request.POST['body'],
                    author = author,
                    repliesTo = postReplied)
            reply.save()

        redirectTo = reverse('thread',
                args = [kwargs['subforum'], kwargs['slug']])
        return HttpResponseRedirect(redirectTo)

class ThreadCreateView(LoginRequiredMixin, CreateView):
    # shows all posts replying to a given thread

    template_name = 'new_thread.html'
    form_class = ThreadForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        subforum_obj = Subforum.objects.get(path=kwargs['subforum'])
        # author_obj = User.objects.get(pk=request.user.id)

        thread = Thread(title = request.POST['title'],
                body = request.POST['body'],
                author = self.request.user,
                subforum = subforum_obj,
                slug = slugify(request.POST['title']),
                )
        thread.save()

        # redirect to /<subforum>/<thread>/
        redirectTo = '/' + kwargs['subforum'] + '/' + thread.slug
        return HttpResponseRedirect(redirectTo)

class ThreadEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Thread
    fields = ('body', )
    template_name = 'thread_edit.html'

    def get_object(self):
        return Thread.objects.get(slug=self.kwargs['slug'])

    def get_success_url(self):
        subforum_slug = self.kwargs['subforum']
        thread_slug = self.kwargs['slug']
        return reverse('thread',
                args=[subforum_slug, thread_slug])

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post
    fields = ('body', )
    template_name = 'post_edit.html'

    def get_object(self):
        return Post.objects.get(id=self.kwargs['pid'])

    def get_success_url(self):
        subforum_slug = self.kwargs['subforum']
        thread_slug = self.kwargs['slug']
        return reverse('thread', 
                args=[subforum_slug, thread_slug])

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ThreadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # this probably doesnt need to inherit DeleteView
    model = Thread
    template_name = 'thread_delete.html'

    def get_object(self):
        return Thread.objects.get(slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse('subforum', args=[self.kwargs['subforum']])
        
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_sentinel_user(self):
        return get_user_model().objects.get_or_create(
                username="[deleted]")[0]

    def post(self, request, *args, **kwargs):
        thread = self.get_object()
        comments = Post.objects.get(thread=thread)

        thread.author = self.get_sentinel_user()
        thread.save() 

        return HttpResponseRedirect(self.get_success_url())

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # this probably doesnt need to inherit DeleteView
    model = Post
    template_name = 'post_delete.html'

    def get_success_url(self):
        subforum_slug = self.kwargs['subforum']
        thread_slug = self.kwargs['slug']
        return reverse('thread', 
                args=[subforum_slug, thread_slug])

    def get_object(self):
        return Post.objects.get(id=self.kwargs['pid'])

    def get_sentinel_user(self):
        return get_user_model().objects.get_or_create(
                username="[deleted]")[0]

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        sentinel = self.get_sentinel_user()

        post.author = sentinel
        post.save()

        return HttpResponseRedirect(self.get_success_url())
