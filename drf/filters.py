import django_filters
from django_filters import rest_framework as filters

from drf.models import Bookinfo


class BookFilter(django_filters.FilterSet):
    image = filters.CharFilter('bimage', method='filter_empty_string')

    class Meta:
        # filed_name='bread' 模型中的字段名；lookup_expr是运算，gte表示>=
        min_read = filters.NumberFilter(field_name='bread', lookup_expr='gte')
        max_read = filters.NumberFilter(field_name='bread', lookup_expr='let')
        model = Bookinfo
        fields = {
            'btitle': ['icontains'],  # 键是字段名，列表里是查询进行运算
            'bcomment': ['lt', 'gt', 'in'],
            'bpub_date': ['exact', 'gt', 'year__lt', 'year__gt'],
            'bimage': ['isnull']
        }

    def filter_empty_string(self, queryset, name, value):
        return queryset.filter(bimage='')
# 127.0.0.1:8000/books/?btitle__icontains=笑
# 127.0.0.1:8000/books/?min_read=30&max_read=80
# 127.0.0.1:8000/books/?bcomment__in=20,30
# 127.0.0.1:8000/books/?path=''
