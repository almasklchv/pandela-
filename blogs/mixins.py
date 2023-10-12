from django.shortcuts import get_object_or_404
from .models import Blog


class MultipleFieldLookupMixin:
    """
    Mixin to filter comments based on slug and id
    """

    def get_object(self, pk):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        # for field in self.lookup_fields:
        #     if self.kwargs[field]: # Ignore empty fields.
        #         filter[field] = self.kwargs[field]
        parent_id = Blog.videoobjects.get(id=pk).id
        filter["parent"] = parent_id
        filter["id"] = self.kwargs["id"]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)

        #тут могут ошибки из-за того что тут был слаг а я все захерачил как pk  +  parent id сам id разобраться надо
        return obj
