from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('<int:pk>', BookDetailView.as_view(), name='book-detail'),
    path('create', BookListCreateView.as_view(), name='book-detail'),
    # path('update', BookListUpdateView.as_view(), name='book-detail'),
    path('highscore/<int:pk>', high_score, name='highscore'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
