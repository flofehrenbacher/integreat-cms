from django import forms
from django.db.models import Q
from django.db.models.query import QuerySet


class ObjectSearchForm(forms.Form):
    """
    Form for searching objects
    """

    query = forms.CharField(min_length=1, required=False)

    search_fields: list[str] = []  # override in child class

    def apply_filters(self, queryset: QuerySet) -> QuerySet:
        search_query = self.cleaned_data.get("query")
        if search_query and self.search_fields:
            q = Q()
            for field in self.search_fields:
                q |= Q(**{f"{field}__icontains": search_query})
            queryset = queryset.filter(q)
        return queryset
