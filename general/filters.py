
import django_filters

from general.models import Post, Profile, Category


class UserFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_expr='icontains', label="Przepis")
    class Meta:
        model = Post
        fields = ['description']



class UserFilter_2(django_filters.FilterSet):
    user_id__username = django_filters.CharFilter(lookup_expr='icontains', label="Login")
    class Meta:
        model = Profile
        fields = ['user_id__username']