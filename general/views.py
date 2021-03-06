from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Count
from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect

from general.filters import UserFilter, UserFilter_2
from general.forms import LoginForm, AddUserForm, ChangePasswordForm, ChangePhotoForm, AddCommentForm, EditPostForm, \
    AddPostForm, DeletePostForm
from general.models import Profile, Post, Comment, Category, Rewrite, Follower

from django.core.files.storage import default_storage


class MainPageView(View):
    def get(self, request):
        post_list = Post.objects.all()
        post_filter = UserFilter(request.GET, queryset=post_list)
        own = request.user
        return render(request, "index.html",
                      {
                          "filter": post_filter,
                          "own": own
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
            Profile.objects.create(user_id=new_user.pk, avatar=photo)
        else:
            Profile.objects.create(user_id=new_user.pk)
        if password != password_2:
            message = "Please repeat password correctly"
            return render(request, "add_user.html", {
                "form": form,
                "message": message
            })
        return redirect('login')


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
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
        profile = Profile.objects.get(user=user_id)
        user_photo = profile.avatar
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(author_id=user_id)
        own = request.user
        number_of_following_my = Follower.objects.filter(follower_user_id=own.id).count()
        number_of_followers_my = Follower.objects.filter(user_id=own.id).count()
        number_of_following = Follower.objects.filter(follower_user_id=user_id).count()
        number_of_followers = Follower.objects.filter(user_id=user_id).count()
        ctx = {
            "user_photo": user_photo,
            "user": user,
            "own": own,
            "number_of_following": number_of_following,
            "number_of_followers": number_of_followers,
            "number_of_following_my": number_of_following_my,
            "number_of_followers_my": number_of_followers_my
        }

        if own.id == user_id:
            if posts:
                ctx['posts'] = posts
                return render(request, "profile.html", ctx)

            return render(request, "profile.html", ctx)
        else:
            if posts:
                ctx['posts'] = posts
                ctx['can_follow'] = not Follower.objects.filter(user_id=user_id, follower_user_id=own.id).exists()
                return render(request, "profile.html", ctx)
            ctx['can_follow'] = not Follower.objects.filter(user_id=user_id, follower_user_id=own.id).exists()
            return render(request, "profile.html", ctx)


class ProfilePictureEdit(LoginRequiredMixin, View):
    def get(self, request, user_id):
        profile = Profile.objects.get(user=user_id)
        user = User.objects.get(id=user_id)
        own = request.user
        ctx = {
            "form": ChangePhotoForm(),
            "user": user,
            "profile": profile,
            "own": own
        }
        return render(request, "change-profile-picture.html", ctx)

    def post(self, request, user_id):
        profile = Profile.objects.get(user=user_id)
        user = User.objects.get(id=user_id)
        form = ChangePhotoForm(request.POST, request.FILES)
        own = request.user
        if not form.is_valid():
            ctx = {
                "form": ChangePhotoForm(),
                "user": user,
                "profile": profile,
                "own": own
            }
            return render(request, "change-profile-picture.html", ctx)
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
        user = User.objects.get(id=user_id)
        form = AddPostForm()
        return render(request, "add-post.html", {
            "user": user,
            "form": form
        })

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        form = AddPostForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, 'Post nie został dodany, spróbuj jeszcze raz')
            return render(request, "add-post.html", {
                "user": user,
                "form": form
            })
        image = request.FILES.get('image')
        description = form.cleaned_data['description']
        recipe = form.cleaned_data['recipe']
        categories = form.cleaned_data['category']
        if image is not None:
            photo = image.name
            with default_storage.open('static/media/' + photo, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                    new_post = Post.objects.create(author_id=user_id, image=photo, description=description, recipe=recipe)
                    for category in categories:
                        new_category=Category.objects.get(category=category)
                        new_post.category.add(new_category)
        else:
            messages.add_message(request, messages.WARNING, 'Dodaj zdjęcie.')
        messages.add_message(request, messages.SUCCESS, 'Post został dodany')
        return redirect(reverse('your-profile', kwargs={"user_id": user.id}))


class EditPostView(LoginRequiredMixin, View):
    def get(self, request, user_id, post_id):
        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        form = EditPostForm(instance=post)
        return render(request, "edit-post.html", {
            "user": user,
            "form": form,
            "post": post
        })

    def post(self, request, user_id, post_id):
        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, 'Post nie został zmodyfikowany, spróbuj jeszcze raz')
            return render(request, "edit-post.html", {
                "user": user,
                "form": form,
                "post": post
            })
        image = request.FILES.get('image')
        updated_post = form.save(commit=False)
        if image:
            photo = image.name
            with default_storage.open('static/media/' + photo, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
        updated_post.author_id=user_id
        updated_post.image = photo
        categories = form.cleaned_data['category']
        post.category.clear()
        for category in categories:
            post.category.add(category)

        updated_post.save()
        messages.add_message(request, messages.SUCCESS, 'Post został zmodyfikowany')
        return redirect(reverse('your-profile', kwargs={"user_id": user.id}))


class DeletePostView(LoginRequiredMixin, View):
    def get(self, request, user_id, post_id):
        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        form = DeletePostForm(instance=post)
        return render(request, "delete-post.html", {
            "user": user,
            "form": form,
            "post": post
        })

    def post(self, request, user_id, post_id):
        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        if post:
            post.delete()
        messages.add_message(request, messages.SUCCESS, 'Post został usunięty')
        return redirect(reverse('your-profile', kwargs={"user_id": user.id}))


class DetailPostView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post_id=post_id)
        own = request.user
        rewrite = Rewrite.objects.filter(user_id=own.id, post_id=post_id)
        number = len(Rewrite.objects.filter(post_id=post_id))
        ctx = {
            "post": post,
            "comments": comments,
            "number": number,
            "own": own
        }
        if own.id == post.author_id:
            ctx['mine'] = "mine"
            return render(request, "detail-post.html", ctx)
        if rewrite:
            ctx['remove'] = "remove"
            return render(request, "detail-post.html", ctx)
        else:
            return render(request, "detail-post.html", ctx)

    def post(self, request, post_id):
        rewrite = request.POST.get('rewrite')
        post = Post.objects.get(id=post_id)
        user = request.user
        comments = Comment.objects.filter(post_id=post_id)
        own = request.user
        ctx = {
            "post": post,
            "comments": comments,
            "own": own
        }
        try:
            if rewrite == "delete":
                rewrited = Rewrite.objects.filter(user_id=user.id, post_id=post_id)
                rewrited.delete()
                number = len(Rewrite.objects.filter(post_id=post_id))
                ctx['number'] = number
                return render(request, "detail-post.html", ctx)
            else:
                new_rewrite = Rewrite.objects.create(user_id=user.id, post_id=post_id)
                new_rewrite.save()
                number = len(Rewrite.objects.filter(post_id=post_id))
                ctx['number'] = number
                ctx['remove'] = 'remove'
                return render(request, "detail-post.html", ctx)

        except IntegrityError:
            number = len(Rewrite.objects.filter(post_id=post_id))
            ctx['remove'] = 'remove'
            ctx['number'] = number
            return render(request, "detail-post.html", ctx)


class OtherPostsView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        profile = Profile.objects.get(user=user_id)
        user_photo = profile.avatar
        user = User.objects.get(id=user_id)
        own = request.user
        rewrites = Rewrite.objects.filter(user_id=user_id)
        number_of_following_my = Follower.objects.filter(follower_user_id=own.id).count()
        number_of_followers_my = Follower.objects.filter(user_id=own.id).count()
        number_of_following = Follower.objects.filter(follower_user_id=user_id).count()
        number_of_followers = Follower.objects.filter(user_id=user_id).count()
        ctx = {
            "user_photo": user_photo,
            "user": user,
            "own": own,
            "number_of_following": number_of_following,
            "number_of_followers": number_of_followers,
            "number_of_following_my": number_of_following_my,
            "number_of_followers_my": number_of_followers_my
        }
        if own.id == user_id:
            if rewrites:
                ctx['rewrites'] = rewrites
                return render(request, "others-posts.html", ctx)

            return render(request, "others-posts.html", ctx)
        else:
            if rewrites:
                ctx['rewrites'] = rewrites
                ctx['can_follow'] = not Follower.objects.filter(user_id=user_id, follower_user_id=own.id).exists()
                return render(request, "others-posts.html", ctx)

            ctx['can_follow'] = not Follower.objects.filter(user_id=user_id, follower_user_id=own.id).exists()
            return render(request, "others-posts.html", ctx)


class AllProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile_list = Profile.objects.all()
        profile_filter = UserFilter_2(request.GET, queryset=profile_list)
        own = request.user
        return render(request, "profiles.html",
                      {
                          "filter": profile_filter,
                          "own": own
                      })


class AddCommentView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        form = AddCommentForm()
        post = Post.objects.get(id=post_id)
        user = post.author.user
        return render(request, "add-comment.html", {
            "form": form,
            "post": post,
            "user": user
        })

    def post(self, request, post_id):
        form = AddCommentForm(request.POST)
        post = Post.objects.get(id=post_id)
        user = post.author.user
        if not form.is_valid():
            messages.add_message(request, messages.WARNING, 'Komentarz nie został dodany, spróbuj jeszcze raz')
            return render(request, "add-comment.html", {
                "user": user,
                "form": form,
                "post": post
            })
        new_comment = form.save(commit=False)
        new_comment.author_id = user.id
        new_comment.post_id = post_id
        new_comment.save()
        messages.add_message(request, messages.SUCCESS, 'Komentarz został dodany')
        return redirect(reverse('details', kwargs={"post_id": post_id}))


class AddFollowerView(LoginRequiredMixin, View):

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.add_message(
                request,
                messages.WARNING,
                'Nie ma takiego użytkownika.'
            )
            return redirect(reverse('your-profile', kwargs={"user_id": user.id}))
        follower_user = request.user
        try:
            Follower.objects.get(user_id=user_id, follower_user_id=follower_user.id).delete()

        except Follower.DoesNotExist:
            Follower.objects.create(user_id=user_id, follower_user_id=follower_user.id)

        except Follower.MultipleObjectsReturned:
            Follower.objects.filter(user_id=user_id, follower_user_id=follower_user.id).delete()

        return redirect(reverse('your-profile', kwargs={"user_id": user.id}))



class TopView(LoginRequiredMixin, View):
    def get(self, request):
        repeated = Rewrite.objects.values('post').annotate(Count('id')).order_by('-id__count').filter(id__count__gt=0)[:10]
        posts = Post.objects.all()
        own = request.user
        return render(request, "top.html",
                      {
                          "repeated": repeated,
                          "posts": posts,
                          "own": own
                      })


class FollowersView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        profile = Profile.objects.get(user=user_id)
        user_photo = profile.avatar
        user = User.objects.get(id=user_id)
        own = request.user
        followers = Follower.objects.filter(follower_user_id=user_id)
        number_of_following_my = Follower.objects.filter(follower_user_id=own.id).count()
        number_of_followers_my = Follower.objects.filter(user_id=own.id).count()
        number_of_following = Follower.objects.filter(follower_user_id=user_id).count()
        number_of_followers = Follower.objects.filter(user_id=user_id).count()
        ctx = {
            "user_photo": user_photo,
            "user": user,
            "own": own,
            "number_of_following": number_of_following,
            "number_of_followers": number_of_followers,
            "number_of_following_my": number_of_following_my,
            "number_of_followers_my": number_of_followers_my
        }

        if own.id == user_id:
            if followers:
                ctx['followers'] = followers
                return render(request, "followers.html", ctx)

            return render(request, "followers.html", ctx)
        else:
            if followers:
                ctx['followers'] = followers
                ctx['can_follow'] = not Follower.objects.filter(user_id=user_id, follower_user_id=own.id).exists()
                return render(request, "followers.html", ctx)

            ctx['can_follow'] = not Follower.objects.filter(user_id=user_id, follower_user_id=own.id).exists()
            return render(request, "followers.html", ctx)


class FollowingsView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        profile = Profile.objects.get(user=user_id)
        user_photo = profile.avatar
        user = User.objects.get(id=user_id)
        own = request.user
        followings = Follower.objects.filter(user_id=user_id)
        number_of_following_my = Follower.objects.filter(follower_user_id=own.id).count()
        number_of_followers_my = Follower.objects.filter(user_id=own.id).count()
        number_of_following = Follower.objects.filter(follower_user_id=user_id).count()
        number_of_followers = Follower.objects.filter(user_id=user_id).count()
        ctx = {
            "user_photo": user_photo,
            "user": user,
            "own": own,
            "number_of_following": number_of_following,
            "number_of_followers": number_of_followers,
            "number_of_following_my": number_of_following_my,
            "number_of_followers_my": number_of_followers_my
        }
        if own.id == user_id:
            if followings:
                ctx ['followings'] = followings
                return render(request, "following.html", ctx)

            return render(request, "following.html", ctx)
        else:
            if followings:
                ctx['followings'] = followings
                ctx['can_follow'] = not Follower.objects.filter(user_id=user_id, follower_user_id=own.id).exists()
                return render(request, "following.html", ctx)

            ctx['can_follow'] = not Follower.objects.filter(user_id=user_id, follower_user_id=own.id).exists()
            return render(request, "following.html", ctx)
