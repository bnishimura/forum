from django.urls import path
from .views import ( HomeView, 
        SubforumView, 
        ThreadCreateView,
        ThreadView,
        )


urlpatterns = [
        path('', HomeView.as_view(), name='home'),
        # SubforumView is a list of threads
        path('<subforum>/', SubforumView.as_view(), name='subforum'),
        # ThreadView is a list with the original post and the replies
        path('<subforum>/new_thread/', ThreadCreateView.as_view(), name='new_thread'),
        path('<subforum>/<slug:slug>/', ThreadView.as_view(), name='thread'),
        ]
