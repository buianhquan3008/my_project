from rest_framework import serializers
from ..models import Book, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)

    class Meta:
        model = Book
        fields = [
            'id',
            'category',
            'name',
            'author',
            'description',
        ]

        extra_kwargs = {'author': {'write_only': True}}


class BookV2Serializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='book-detail', format='html')

    class Meta:
        model = Book
        fields = ['url', 'name', 'author']
        read_only_fields = fields
        extra_kwargs = {
            'url': {'view_name': 'api-book:book-detail'},
        }
