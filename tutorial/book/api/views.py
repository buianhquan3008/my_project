from ..models import Book, HighScore
from .serializers import BookSerializer, BookV2Serializer, HighScoreSerializer
from rest_framework import generics
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.decorators import api_view


class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookV2Serializer


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListCreateView(generics.CreateAPIView, CreateModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(BookListCreateView, self).get_serializer(*args, **kwargs)


# class BookListUpdateView(generics.UpdateAPIView, UpdateModelMixin):
#     serializer_class = BookSerializer
#     queryset = Book.objects.all()
#
#     def get_serializer(self, *args, **kwargs):
#         if isinstance(kwargs.get("data", {}), list):
#             kwargs["many"] = True
#
#         return super(BookListUpdateView, self).get_serializer(*args, **kwargs)


@api_view(['GET'])
def high_score(request, pk):
    instance = HighScore.objects.get(pk=pk)
    serializer = HighScoreSerializer(instance)
    return Response(serializer.data)
