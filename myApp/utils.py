from django.core.paginator import Paginator


class CustomPaginator(Paginator):
    def lst(self, page):
        return self.page(page).object_list
