from django import template
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, View
from django.contrib.auth.models import User
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
        context = { 'subforum': curr_subforum.path }
        queryset = Thread.objects.filter(subforum__path=path)
        context['thread_list'] = queryset
        return context

class ThreadView(View):

    template_name = 'thread.html'
    form = PostForm()

    def get_replies(self, reply_context, post):
        # appends replies to context
        replies = Post.objects.filter(reply=post.id)
        if replies:
            reply_context[post.id] = replies
            for reply in replies:
                self.get_replies(reply_context, reply)

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
        context['replies'] = reply_context

        t = template.loader.get_template(self.template_name)
        return HttpResponse(t.render(context, request=request))

    def post(self, request, *args, **kwargs):
        '''
        We differentiate posts and replies even though they are
        both instances of Post
        '''
        author = User.objects.get(id=request.POST['author'])
        print(request.POST)

        if 'thread_reply' in request.POST:
            threadReplied = Thread.objects.get(id=request.POST['thread_reply'])

            post = Post(body = request.POST['body'],
                    author = author,
                    thread = threadReplied)
            post.save()

        elif 'post_reply' in request.POST:
            postReplied = Post.objects.get(id=request.POST['post_reply'])
            reply = Post(body = request.POST['body'],
                    author = author,
                    reply = postReplied)
            reply.save()

        redirectTo = reverse('thread',
                args = [kwargs['subforum'], kwargs['slug']])
        print(redirectTo)
        return HttpResponseRedirect(redirectTo)

class ThreadCreateView(CreateView):
    # shows all posts replying to a given thread

    template_name = 'new_thread.html'
    form_class = ThreadForm

    def post(self, request, *args, **kwargs):
        subforum_obj = Subforum.objects.get(title=kwargs['subforum'])
        # form is getting a user_id THIS HAS TO BE DELETED LATER
        author_obj = User.objects.get(pk=request.POST['author'])

        # remove author later
        thread = Thread(title = request.POST['title'],
                body = request.POST['body'],
                author = author_obj,
                subforum = subforum_obj,
                slug = slugify(request.POST['body']),
                )
        thread.save()

        # redirect to /<subforum>/<thread>/
        redirectTo = '/' + kwargs['subforum'] + '/' + thread.slug
        return HttpResponseRedirect(redirectTo)
