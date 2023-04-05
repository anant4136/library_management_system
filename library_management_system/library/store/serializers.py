from rest_framework import serializers
from .models import Book, BookOrder, User, Bookmark
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'email',
                  'phone', 'is_staff', 'location']
        extra_kwargs = {'password': {'write_only': True}}


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'name',
                  'phone', 'is_staff', 'location']


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'name', )


class BookDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'name', 'author', 'mrp', )


class OrderBookSerializer(serializers.Serializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    def save(self):
        book = self.validated_data['book']
        user = self.context['request'].user
        order, created = BookOrder.objects.get_or_create(customer=user)
        if order.books.filter(id=book.id):
            raise serializers.ValidationError("Book already loaned")
        order.books.add(book)
        return order


class ReturnBookSerializer(serializers.Serializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    def remove(self):
        book = self.validated_data['book']
        user = self.context['request'].user
        order, created = BookOrder.objects.get_or_create(customer=user)
        if not order.books.filter(id=book.id):
            raise serializers.ValidationError("Book not loaned")
        order.books.remove(book)
        return order


class BookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'book']
        read_only_fields = ['id', 'user']


class BookmarkDetailSerializer(serializers.ModelSerializer):
    machine = BookDetailSerializer()

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'book']
        read_only_fields = ['id', 'user']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(
        max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(
        max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        print(value)
        if not user.check_password(value):
            raise serializers.ValidationError(
                ('Your old password was entered incorrectly. Please enter it again.')
            )
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError(
                {'new_password2': ("The two password fields didn't match.")})
        password_validation.validate_password(
            data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user
