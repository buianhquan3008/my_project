from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path('', BookList.as_view(), name='book-list'),
    path('<int:pk>', BookDetail.as_view(), name='book-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
