"""foodsy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from general.views import LoginView, MainPageView, AddUserView, logout_view, ChangePasswordView, ProfileView, \
    ProfilePictureEdit, DeletePostView, DetailPostView, OtherPostsView, AllProfileView, \
    AddCommentView, EditPostView, AddPostView, AddFollowerView \
    # , TopView, FollowersView, FollowingsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
    path('reset_password/<int:user_id>', ChangePasswordView.as_view(), name="change-password"),
    path('registration/', AddUserView.as_view(), name="registration"),
    path('your-profile/<int:user_id>', ProfileView.as_view(), name="your-profile"),
    path('your-profile/<int:user_id>/change-photo', ProfilePictureEdit.as_view(), name="change-photo"),
    path('your-profile/<int:user_id>/add-post', AddPostView.as_view(), name="add-post"),
    path('your-profile/<int:user_id>/edit-post/<int:post_id>', EditPostView.as_view(), name="edit-post"),
    path('your-profile/<int:user_id>/delete-post/<int:post_id>', DeletePostView.as_view(), name="delete-post"),
    path('your-profile/<int:user_id>/follow', AddFollowerView.as_view(), name="follow"),
    path('your-profile/<int:user_id>/other-posts/', OtherPostsView.as_view(), name="others"),
    # path('your-profile/<int:user_id>/followers/', FollowersView.as_view(), name="followers"),
    # path('your-profile/<int:user_id>/followings/', FollowingsView.as_view(), name="followings"),
    path('profiles/', AllProfileView.as_view(), name="profiles"),
    path('details/<int:post_id>', DetailPostView.as_view(), name="details"),
    path('details/<int:post_id>/add-comment', AddCommentView.as_view(), name="add-comment"),
    # path('top/', TopView.as_view(), name="top"),


]

