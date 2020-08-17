from rest_framework import serializers
from ..models import Book, Category, DataPoint
import re
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class BookListSerializer(serializers.ListSerializer):
    # def create(self, validated_data):
    #     books = [Book(**item) for item in validated_data]
    #     return Book.objects.bulk_create(books)

    def create(self, validated_data):
        # Maps for id->instance and id->data item.
        instance = Book.objects.all()
        book_mapping = {book.id: book for book in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for book_id, data in data_mapping.items():
            book = book_mapping.get(book_id, None)
            if book is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(book, data))

        # Perform deletions.
        for book_id, book in book_mapping.items():
            if book_id not in data_mapping:
                book.delete()

        return ret

    @classmethod
    def many_init(cls, *args, **kwargs):
        # Instantiate the child serializer.
        kwargs['child'] = cls()
        # Instantiate the parent list serializer.
        return BookListSerializer(*args, **kwargs)


class BookSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(required=False)
    id = serializers.IntegerField()

    class Meta:
        model = Book
        fields = [
            'id',
            'category',
            'name',
            'author',
            'description',
        ]
        # read_only_fields = ['id']
        list_serializer_class = BookListSerializer
        extra_kwargs = {'author': {'write_only': True}}


class BookV2Serializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Book
        fields = ['url', 'name', 'author']
        read_only_fields = fields
        extra_kwargs = {
            'url': {'view_name': 'api-book:book-detail'},
        }


class HighScoreSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'score': instance.score,
            'player_name': instance.player_name,
        }


class Color:
    """
    A color represented in the RGB colorspace.
    """
    def __init__(self, red, green, blue):
        assert(red >= 0 and green >= 0 and blue >= 0)
        assert(red < 256 and green < 256 and blue < 256)
        self.red, self.green, self.blue = red, green, blue


class ColorField(serializers.Field):
    """
    Color objects are serialized into 'rgb(#, #, #)' notation.
    (example for serializer field custom)
    """
    def to_representation(self, value):
        return "rgb(%d, %d, %d)" % (value.red, value.green, value.blue)

    def to_internal_value(self, data):
        # data = data.strip('rgb(').rstrip(')')
        # red, green, blue = [int(col) for col in data.split(',')]
        # return Color(red, green, blue)

        """validate"""
        if not isinstance(data, str):
            msg = 'Incorrect type. Expected a string, but got %s'
            raise ValidationError(msg % type(data).__name__)

        if not re.match(r'^rgb\([0-9]+,[0-9]+,[0-9]+\)$', data):
            raise ValidationError('Incorrect format. Expected `rgb(#,#,#)`.')

        data = data.strip('rgb(').rstrip(')')
        red, green, blue = [int(col) for col in data.split(',')]

        if any([col > 255 or col < 0 for col in (red, green, blue)]):
            raise ValidationError('Value out of range. Must be between 0 and 255.')

        return Color(red, green, blue)


class CoordinateField(serializers.Field):

    def to_representation(self, value):
        ret = {
            "x": value.x_coordinate,
            "y": value.y_coordinate,
        }
        return ret

    def to_internal_value(self, data):
        ret = {
            "x_coordinate": data["x"],
            "y_coordinate": data["y"],
        }
        return ret


class DataPointSerializer(serializers.ModelSerializer):
    coordinates = CoordinateField(source='*')
    color = ColorField()

    class Meta:
        model = DataPoint
        fields = ['label', 'coordinates']
