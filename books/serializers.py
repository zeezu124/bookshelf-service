from rest_framework import serializers

class LibrarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    book_ids = serializers.ListField(child=serializers.CharField())

class BookSerializer(serializers.Serializer):
    book_id = serializers.CharField()

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()