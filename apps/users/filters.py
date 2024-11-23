from django_filters import FilterSet, BooleanFilter, NumberFilter, CharFilter

from apps.users.models import Doctor, DoctorCategory


class TopDoctor(FilterSet):
    category = CharFilter(method='filter_by_category')
    top = BooleanFilter(method='filter_top', label='Top Doctors')
    min_score = NumberFilter(field_name='score', lookup_expr='gte', label='Minimum Score')
    max_score = NumberFilter(field_name='score', lookup_expr='lte', label='Maximum Score')

    class Meta:
        model = Doctor
        fields = ['top', 'min_score', 'max_score', 'category']

    def filter_by_category(self, queryset, field, value):
        matching_categories = DoctorCategory.objects.filter(name__icontains=value)

        return queryset.filter(
            category__in=list(matching_categories)
        )

    def filter_top(self, queryset, name, value):
        if value:
            return queryset.order_by('-score')[:2]
        return queryset
