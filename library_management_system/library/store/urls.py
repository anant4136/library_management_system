from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as auth_views
from store import views

urlpatterns = [
    path('register/', views.registerUser.as_view(), name='register'),
    path('users/<int:pk>', views.UsersView.as_view(), name='user'),
    path('users/change-password',
         views.ChangePasswordView.as_view(), name='change-password'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('store/', views.BookList.as_view()),
    path('store/<int:pk>/', views.BookDetail.as_view()),
    path('orders/', views.BookOrderList.as_view()),
    path('order/', views.OrderBook.as_view()),
    path('return/', views.ReturnBook.as_view()),
    path('bookmarks/', views.BookmarkView.as_view(), name='bookmarks'),
    path('bookmarks/<int:pk>', views.BookmarkDetailView.as_view(),
         name='bookmarksdetails'),
    path('token/', auth_views.obtain_auth_token)
]

urlpatterns = format_suffix_patterns(urlpatterns)
