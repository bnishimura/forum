from django.urls import path
from .views import ( HomeView, 
        SubforumView, 
        ThreadCreateView,
        ThreadView,
        ThreadEditView,
        PostEditView,
        ThreadDeleteView,
        PostDeleteView
        )


urlpatterns = [
        path('', HomeView.as_view(), name='home'),
        # SubforumView is a list of threads
        path('<slug:subforum>/', SubforumView.as_view(), name='subforum'),
        # ThreadView is a list with the original post and the replies
        path('<slug:subforum>/new_thread/', ThreadCreateView.as_view(), name='new_thread'),
        path('<slug:subforum>/<slug:slug>/', ThreadView.as_view(), name='thread'),

        # ideally edits in posts and threads should happen on the threadview
        path('<slug:subforum>/<slug:slug>/edit_thread/', ThreadEditView.as_view(), name='edit_thread'),
        path('<slug:subforum>/<slug:slug>/<int:pid>/edit_post/', PostEditView.as_view(), name="edit_post"),

        path('<slug:subforum>/<slug:slug>/delete_thread/', ThreadDeleteView.as_view(), name='delete_thread'),
        path('<slug:subforum>/<slug:slug>/<int:pid>/delete_post/', PostDeleteView.as_view(), name='delete_post'),
        ]
