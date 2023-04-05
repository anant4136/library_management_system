from rest_framework import generics, authentication, permissions, status
from rest_framework.response import Response
from .models import *
from .serializers import BookSerializer, BookDetailSerializer, BookmarkDetailSerializer, BookmarkSerializer, ChangePasswordSerializer, OrderBookSerializer, ReturnBookSerializer, UserSerializer, UserUpdateSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import UpdateAPIView
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
import datetime
from django.conf import settings


class registerUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data
        user = User.objects.create_user(
            data["username"], data["email"], data["password"])
        user.name = data["name"]
        user.is_industry = data["is_industry"]
        user.phone = data["phone"]
        user.location = data["location"]
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UsersView(generics.RetrieveAPIView):
    def get_permissions(self):
        method = self.request.method
        if method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer = UserUpdateSerializer(
            instance=request.user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class OrderBook(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = OrderBookSerializer

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        order = self.serializer.save()
        return Response(status=status.HTTP_200_OK)


class ReturnBook(generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = ReturnBookSerializer

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        order = self.serializer.remove()
        return Response(status=status.HTTP_200_OK)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer


class BookOrderList(generics.GenericAPIView):

    def get(self, request):
        return Response(BookOrder.objects.get(customer=request.user.id).books.values())


class BookmarkView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkSerializer

    def get_serializer_class(self):

        method = self.request.method
        if method == 'GET':
            return BookmarkDetailSerializer
        return BookmarkSerializer

    def get_queryset(self):

        return Bookmark.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)


class BookmarkDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()

    def delete(self, request, **kwargs):

        bookmark = self.get_object()
        if bookmark.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
