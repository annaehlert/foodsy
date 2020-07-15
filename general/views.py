from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect

from general.filters import UserFilter, UserFilter_2
from general.forms import LoginForm, AddUserForm, ChangePasswordForm, ChangePhotoForm, AddPostForm
from general.models import Profile, Post, Category
from django.core.files.storage import default_storage


class MainPageView(View):
    def get(self, request):
        post_list = Post.objects.all()
        post_filter = UserFilter(request.GET, queryset=post_list)
        categories = Category.objects.all()
        return render(request, "index.html",
                      {
                          # "posts": post_list,
                          "filter": post_filter
                      })


class LoginView(View):
    def get(self, request):
        if request.user.id is not None:
            return redirect('index')
        return render(
            request,
            "login.html",
        {"form": LoginForm()}
        )
    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "login.html",
                {"form": form}
            )
        user = authenticate(
            request=request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is None:
            messages.add_message(request, messages.WARNING, 'Profil o podanych danych nie istnieje.')
            return redirect('login')
        login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Zostałeś poprawnie zalogowany.')
        return redirect('index')
        # return redirect(reverse('your-profile', kwargs={"user_id": user.id}))


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


class AddUserView(View):
    def get(self, request):
        if request.user.id is not None:
            return redirect("index")
        return render(request, "add_user.html", {
            "form": AddUserForm()
        })

    def post(self, request):
        form = AddUserForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "add_user.html", {
                "form": form
            })
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        password = form.cleaned_data['password']
        password_2 = form.cleaned_data['password_2']
        image = request.FILES.get('image')
        User.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                 last_name=last_name)
        new_user = User.objects.get(username=username)
        if image is not None:
            photo = image.name
            with default_storage.open('static/media/' + photo, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            Profile.objects.create(user_id_id=new_user.pk, avatar=photo)
        else:
            Profile.objects.create(user_id_id=new_user.pk)
        if password != password_2:
            message = "Please repeat password correctly"
            return render(request, "add_user.html", {
                "form": form,
                "message": message
            })
        return redirect('login')



class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = Profile.objects.get(user_id=user_id)
        return render(request, "change_password.html", {
            "form": ChangePasswordForm(),
            "user": user
        })


    def post(self, request, user_id):
        form = ChangePasswordForm(request.POST)
        if not form.is_valid():
            return render(request, "change_password.html", {
                "form": ChangePasswordForm()
            })
        password = form.cleaned_data['password']
        password_2 = form.cleaned_data['password_2']
        if password != password_2:
            message = "Please repeat password correctly"
            return render(request, "add_user.html", {
                "form": form,
                "message": message
            })
        user = User.objects.get(user_id=user_id)
        user.set_password(password)
        user.save()
        message = "Password changed correctly"
        return render(request, "add_user.html", {
            "message": message
        })


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        profile = Profile.objects.get(user_id=user_id)
        user_photo = profile.avatar
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(author_id=user_id)
        if posts:
            Post.objects.filter(author_id=user_id)
            return render(request, "profile.html", {
                "user_photo": user_photo,
                "user": user,
                "posts": posts,
            })

        return render(request, "profile.html", {
            "user_photo": user_photo,
            "user": user,
        })

class ProfilePictureEdit(LoginRequiredMixin, View):
    def get(self, request, user_id):
        profile = Profile.objects.get(user_id=user_id)
        user = User.objects.get(id=user_id)
        form = ChangePhotoForm()
        return render(request, "change-profile-picture.html", {
            "form": form,
            "user": user
        })
    def post(self, request, user_id):
        profile = Profile.objects.get(user_id=user_id)
        user = User.objects.get(id=user_id)
        form = ChangePhotoForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "change-profile-picture.html", {
                "form": ChangePhotoForm(),
                "user": user
            })
        image = request.FILES.get('image')
        if image is not None:
            photo = image.name
            with default_storage.open('static/media/' + photo, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            profile.avatar = photo
        profile.save()
        return redirect(reverse('your-profile', kwargs={"user_id": user.id}))


class AddPostView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        profile = Profile.objects.get(user_id=user_id)
        user = User.objects.get(id=user_id)
        form = AddPostForm()
        return render(request, "add-post.html", {
            "user": user,
            "form": form
        })

    def post(self, request, user_id):
        profile = Profile.objects.get(user_id=user_id)
        user = User.objects.get(id=user_id)
        form = AddPostForm(request.POST, request.FILES)
        if not form.is_valid():   #muszę dodać message, że coś poszło nie tak!!
            messages.add_message(request, messages.WARNING, 'Post nie został dodany, spróbuj jeszcze raz')
            return render(request, "add-post.html", {
                "user": user,
                "form": form
            })
        new_post = form.save(commit=False)
        image = request.FILES.get('image')
        if image is not None:
            photo = image.name
            with default_storage.open('static/media/' + photo, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
        new_post.author_id = user_id
        new_post.save()
        messages.add_message(request, messages.SUCCESS, 'Post został dodany')
        return redirect(reverse('your-profile', kwargs={"user_id": user.id}))


class EditPostView(LoginRequiredMixin, View):
    def get(self, request, user_id, post_id):
        profile = Profile.objects.get(user_id=user_id)
        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        form = AddPostForm(instance=post)
        return render(request, "edit-post.html", {
            "user": user,
            "form": form,
            "post": post
        })

    def post(self, request, user_id, post_id):
        profile = Profile.objects.get(user_id=user_id)
        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        form = AddPostForm(request.POST, request.FILES, instance=post)
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, 'Post nie został zmodyfikowany, spróbuj jeszcze raz')
            return render(request, "edit-post.html", {
                "user": user,
                "form": form
            })
        post = form.save(commit=False)
        image = request.FILES.get('image')
        if image is not None:
            photo = image.name
            with default_storage.open('static/media/' + photo, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                    post.image = photo
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Post został zmodyfikowany')
        return redirect(reverse('your-profile', kwargs={"user_id": user.id}))


class DeletePostView(LoginRequiredMixin, View):
    def get(self, request, user_id, post_id):
        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        if post:
            post.delete()
        messages.add_message(request, messages.SUCCESS, 'Post został usunięty')
        return redirect(reverse('your-profile', kwargs={"user_id": user.id}))


class DetailPostView(View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        return render(request, "detail-post.html", {
            "post": post
        })


class OtherPostsView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        profile = Profile.objects.get(user_id=user_id)
        user_photo = profile.avatar
        user = User.objects.get(id=user_id)
        posts = Post.objects.exclude(author_id=user_id)
        if posts:
            return render(request, "others-posts.html", {
                "user_photo": user_photo,
                "user": user,
                "posts": posts,
            })
        return render(request, "profile.html", {
            "user_photo": user_photo,
            "user": user,
        })


class AllProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile_list = Profile.objects.all()
        profile_filter = UserFilter_2(request.GET, queryset=profile_list)
        return render(request, "profiles.html",
                      {
                          "filter": profile_filter
                      })

