from rest_framework.pagination import PageNumberPagination

class CustomPaginationForPosts(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ChatPagination(PageNumberPagination):
    page_size = 20  # Number of messages per request
    page_size_query_param = "page_size"
    max_page_size = 50  # Prevent excessive data load