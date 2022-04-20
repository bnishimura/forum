from django.urls import reverse
from django.test import TestCase, Client
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from forum.models import Post, Thread, Subforum, Category
from django.contrib.auth.models import User


def setUp(test_obj):
    test_obj.user = get_user_model().objects.create(
            username = 'sandman')

    test_obj.sentinel = get_user_model().objects.get_or_create(
            username = '[deleted]')[0]

    test_obj.category = Category.objects.create(
            name = 'A category')

    test_obj.subforum = Subforum.objects.create(
            title = 'A subforum',
            description = 'some description',
            category = test_obj.category,
            path = slugify('A subforum'))

    test_obj.thread = Thread.objects.create(
            title = 'A title',
            body = 'some text',
            author = test_obj.user,
            subforum = test_obj.subforum,
            slug = slugify('A title'))

    test_obj.first_post = Post.objects.create(
            body = 'this is a test',
            author = test_obj.user,
            thread = test_obj.thread)

    # replies to posts points to no thread
    test_obj.second_post = Post.objects.create(
            body = 'this is an answer to the first post',
            repliesTo = test_obj.first_post,
            author = test_obj.user)

    test_obj.third_post = Post.objects.create(
            body = 'this is an answer to the second post',
            repliesTo = test_obj.second_post,
            author = test_obj.user)

########################################################
#                   Home Tests
########################################################

class HomeViewTest(TestCase):
    def setUp(self):
        setUp(self)
        self.second_category = Category.objects.create(
                name = 'Second category')

        self.third_category = Category.objects.create(
                name = 'Third category')

        self.first_cat_extra_subforum = Subforum.objects.create(
                title = 'extra first category subforum',
                description = 'This belongs to the first category',
                category = self.category,
                path = slugify('first category subforum'))

        self.second_cat_subforum = Subforum.objects.create(
                title = 'Second category subforum',
                description = 'This belongs to the second category',
                category = self.second_category,
                path = slugify('Second category subforum'))

        self.third_cat_subforum = Subforum.objects.create(
                title = 'Third category subforum',
                description = 'This belongs to the third category',
                category = self.third_category,
                path = slugify('Third category subforum'))

    def test_home_context(self):
        response = self.client.get(reverse('home'))
        home_layout = { 
                self.category.name: [self.subforum, self.first_cat_extra_subforum],
                self.second_category.name: [self.second_cat_subforum],
                self.third_category.name: [self.third_cat_subforum]
                }

        self.assertEqual(response.context['layout'], home_layout)
        self.assertTemplateUsed(response, 'home.html')

########################################################
#                   Subforum Tests
########################################################

class SubforumViewTest(TestCase):
    # the subforum view lists all threads associated with it 
    def setUp(self):
        setUp(self)
        
        new_thread_title = 'another thread title'
        self.another_thread = Thread.objects.create(
                title=new_thread_title,
                body='another thread body',
                author=self.user,
                subforum=self.subforum,
                slug=slugify(new_thread_title))

        self.client.force_login(self.user)

    def test_view_context(self):
        response = self.client.get(reverse('subforum',
            args=[self.subforum.path]))

        self.assertTrue(self.thread in response.context['thread_list'])
        self.assertTrue(self.another_thread in response.context['thread_list'])
        self.assertTemplateUsed(response, 'subforum.html')

########################################################
#                   Post Tests
########################################################

class PostEditTest(TestCase):
    
    def setUp(self):
        setUp(self)
        self.client.force_login(self.user)

    def test_post_edit(self):
        new_body = "new body text"
        response = self.client.post(reverse('edit_post',
            args=[self.subforum.path, self.thread.slug,
                self.third_post.id]),
            data={'body': new_body})
        
        new_third_post = Post.objects.get(id=self.third_post.id)
        self.assertEqual(new_third_post.body, new_body)
        self.assertRedirects(response,
                reverse('thread', args=[self.subforum.path, self.thread.slug]),
                status_code=302,
                target_status_code=200,
                fetch_redirect_response=True)

class PostDeletionTest(TestCase):

    def setUp(self):
        setUp(self)

        # to delete posts, you must login for some reason
        self.client.force_login(self.user)

    def test_post_deletion(self):

        # delete second_post
        response = self.client.post(reverse('delete_post',
            args=[self.subforum.path, self.thread.slug,
                self.second_post.id]))

        # need to query again(self.second_post does not change)
        new_second_post = Post.objects.get(id=self.second_post.id)

        # check if second_post changed
        self.assertEqual(new_second_post.author, self.sentinel)
        # check integrity of other posts
        self.assertNotEqual(self.first_post.author, self.sentinel)
        self.assertNotEqual(self.third_post.author, self.sentinel)

        # see if it redirects successfully
        self.assertRedirects(response,
                reverse('thread', args=[self.subforum.path, self.thread.slug]),
                status_code = 302,
                target_status_code = 200,
                fetch_redirect_response = True)

########################################################
#                   Thread Tests
########################################################

class ThreadViewTest(TestCase):
    def setUp(self):
        setUp(self)
        self.client.force_login(self.user)

    def test_thread_get(self):
        response = self.client.get(reverse('thread',
                args=[self.subforum.path, self.thread.slug]))
        self.assertEqual(response.status_code, 200)

    def test_thread_post_thread_reply(self):
        # tests replies to threads
        post_body = 'nice test thread body'
        thread_reply = {'body': post_body,
                'thread_reply': self.thread.id}
        thread_path = reverse('thread',
            args=[self.subforum.path, self.thread.slug])

        response = self.client.post(path=thread_path,
            data=thread_reply)

        post = Post.objects.get(body=post_body)
        self.assertEqual(post.body, post_body)
        self.assertRedirects(response,
                thread_path,
                status_code=302,
                target_status_code=200,
                fetch_redirect_response=True)

    def test_thread_post_post_reply(self):
        # tests replies to posts inside a thread
        reply_body = 'nice comment, bro'
        post_reply = {'body': reply_body,
                'post_reply': self.first_post.id}
        post_path = reverse('thread',
            args=[self.subforum.path, self.thread.slug])

        response = self.client.post(path=post_path,
            data=post_reply)

        reply = Post.objects.get(body=reply_body)
        self.assertEqual(reply.body, reply_body)
        self.assertEqual(reply.repliesTo, self.first_post)
        self.assertRedirects(response,
                post_path,
                status_code=302,
                target_status_code=200,
                fetch_redirect_response=True)

class ThreadCreateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
                username = 'sandman')

        self.category = Category.objects.create(
                name = 'A category')

        self.subforum = Subforum.objects.create(
                title = 'A subforum',
                description = 'some description',
                category = self.category,
                path = slugify('A subforum'))

        self.client.force_login(self.user)

    def test_thread_creation(self):
        title = 'a special test title'
        body = 'a special test body'
        response = self.client.post(reverse('new_thread',
            args=[self.subforum.path]),
            data={'title': title, 'body': body})

        new_thread = Thread.objects.get(title=title)
        self.assertEqual(new_thread.body, body)

class ThreadEditTest(TestCase):
    def setUp(self):
        setUp(self)
        self.client.force_login(self.user)

    def test_thread_edit(self):
        new_body = 'new thread body'
        response = self.client.post(reverse('edit_thread',
            args=[self.subforum.path, self.thread.slug]),
            data={'body': new_body})

        new_thread = Thread.objects.get(id=self.thread.id)
        self.assertEqual(new_thread.body, new_body)

class ThreadDeletionTest(TestCase):
    def setUp(self):
        setUp(self)
        self.client.force_login(self.user)

    def test_thread_deletion(self):

        response = self.client.post(reverse('delete_thread',
            # can these args become a problem?
            args=[self.subforum.path, self.thread.slug]))
        deleted_thread = Thread.objects.get(id=self.thread.id)

        # test thread deletion
        self.assertEqual(deleted_thread.author, self.sentinel)
        # test successfull redirection
        self.assertRedirects(response,
                reverse('subforum', args=[self.subforum.path]),
                status_code=302,
                target_status_code=200,
                fetch_redirect_response=True)
