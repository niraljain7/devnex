from rest_framework import serializers
from library.models import Author, Book, BorrowRecord
from django.utils.timezone import now

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author_details = AuthorSerializer(source='author', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_details', 'isbn', 'available_copies']

class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'borrowed_by', 'borrow_date']

    def validate(self, data):
        borrow_date = data.get('borrow_date')

        if borrow_date > now().date():
            raise serializers.ValidationError("Borrow date cannot be in the future.")

        return data
