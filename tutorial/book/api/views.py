from ..models import Book
from .serializers import BookSerializer, BookV2Serializer
from rest_framework import generics


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookV2Serializer


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

