from rest_framework.pagination import PageNumberPagination


class TokenListAPIViewPagination(PageNumberPagination):
    page_size = 200
    max_page_size = 500
    page_size_query_param = 'page_size'
    page_query_param = 'page'
