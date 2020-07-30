import django_filters
from django import forms

from general.models import Post, Profile, Category


class UserFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_expr='icontains', label="Przepis")
    category = django_filters.ModelMultipleChoiceFilter(
        label="Kategoria",
        widget=forms.CheckboxSelectMultiple,
        queryset=Category.objects.all(),
        field_name='attr__category',
        to_field_name='category',
    )

    class Meta:
        model = Post
        fields = ['description', 'category']


class UserFilter_2(django_filters.FilterSet):
    user_id__username = django_filters.CharFilter(lookup_expr='icontains', label="Login")

    class Meta:
        model = Profile
        fields = ['user_id__username']