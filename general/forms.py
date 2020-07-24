from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelMultipleChoiceField

from general.models import Post, Comment, Category


class LoginForm(forms.Form):
    username = forms.CharField(label="Login", max_length=100)
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)


def validate_password(value):
    if value.islower() or value.isalpha() or value.isdigit() or len(value) <= 7:
        raise ValidationError(
            "Twoje hasło musi zawierać wielką literę, małą literę, cyfrę oraz mieć conajmniej 7 znaków.")


class AddUserForm(forms.Form):
    username = forms.CharField(label="Login", max_length=40)
    password = forms.CharField(label="Hasło", max_length=40, widget=forms.PasswordInput, validators=[validate_password])
    password_2 = forms.CharField(label="Powtórz hasło", max_length=40, widget=forms.PasswordInput,
                                 validators=[validate_password])
    email = forms.EmailField(label="Email", max_length=60, widget=forms.EmailInput)
    first_name = forms.CharField(label="Imię", max_length=60)
    last_name = forms.CharField(label="Nazwisko", max_length=60)
    image = forms.ImageField(label="Zdjęcie profilowe", required=False)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label="Nowe hasło", max_length=40, widget=forms.PasswordInput,
                               validators=[validate_password])
    password_2 = forms.CharField(label="Powtórz nowe hasło", max_length=40, widget=forms.PasswordInput,
                                 validators=[validate_password])


class ChangePhotoForm(forms.Form):
    image = forms.ImageField(label="Zdjęcie profilowe", required=False)


class AddPostForm(forms.Form):
    image = forms.ImageField(label="Zdjęcie")
    description = forms.CharField(max_length=255, label="nazwa przepisu")
    recipe = forms.CharField(label="przepis", widget=forms.Textarea)
    category = forms.MultipleChoiceField(
        label="kategoria",
        widget=forms.CheckboxSelectMultiple,
        choices=[(c.pk, c.category) for c in Category.objects.all()]
    )


class CategoryMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.category


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'description', 'recipe', 'category']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('category', None)
        super(EditPostForm, self).__init__(*args, **kwargs)
        self.fields['category'] = CategoryMultipleChoiceField(
            label="kategoria",
            widget=forms.CheckboxSelectMultiple,
            queryset=Category.objects.all()
        )


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

