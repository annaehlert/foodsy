from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render, redirect

from general.forms import LoginForm, AddUserForm
from general.models import Users
from django.core.files.storage import default_storage


class MainPageView(View):
    def get(self, request):
        return render(request, "index.html")


class LoginView(View):
    def get(self, request):
        if request.user.id is not None:
            return redirect('login')
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
            messages.add_message(request, messages.WARNING, 'User does not exist')
            return redirect('login')
        login(request, user)
        messages.add_message(request, messages.SUCCESS, 'User logged in successfully')
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
        image = request.FILES['image']
        photo = image.name
        if password != password_2:
            message = "Please repeat password correctly"
            return render(request, "add_user.html", {
                "form": form,
                "message": message
            })
        with default_storage.open('static/media/' + photo, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        new_user = User.objects.get(username=username)
        Users.objects.create(user_id_id=new_user.pk, avatar=photo)
        return redirect('login')



# class ChangePasswordView(View):
#     def get(self, request, user_id):
#         user = User.objects.get(id=user_id)
#         return render(request, "exercises/change_password.html", {
#             "form": ChangePasswordForm(),
#             "user": user
#         })
#
#
#     def post(self, request, user_id):
#         form = ChangePasswordForm(request.POST)
#         if not form.is_valid():
#             return render(request, "exercises/change_password.html", {
#                 "form": ChangePasswordForm()
#             })
#         password = form.cleaned_data['password']
#         password_2 = form.cleaned_data['password_2']
#         if password != password_2:
#             message = "Please repeat password correctly"
#             return render(request, "exercises/add_user.html", {
#                 "form": form,
#                 "message": message
#             })
#         user = User.objects.get(id=user_id)
#         user.set_password(password)
#         user.save()
#         message = "Password changed correctly"
#         return render(request, "exercises/add_user.html", {
#             "message": message
#         })
