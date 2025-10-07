from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomPagination(pagination.PageNumberPagination):
    """
    Custom pagination class với định dạng response tùy chỉnh
    """
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('links', OrderedDict([
                ('previous', self.get_previous_link()),
                ('next', self.get_next_link()),
            ])),
            ('page', self.page.number),
            ('page_size', self.get_page_size(self.request)),
            ('num_pages', self.page.paginator.num_pages),
            ('count', self.page.paginator.count),
            ('results', data),
        ]))


class StandardPagination(pagination.PageNumberPagination):
    """
    Standard pagination cho các API thông thường
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 1000


class LargePagination(pagination.PageNumberPagination):
    """
    Pagination cho các tập dữ liệu lớn
    """
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 500


class SmallPagination(pagination.PageNumberPagination):
    """
    Pagination cho mobile apps hoặc hiển thị ít item
    """
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class LimitOffsetCustomPagination(pagination.LimitOffsetPagination):
    """
    Pagination sử dụng limit/offset thay vì page
    URL: /api/employees/?limit=20&offset=40
    """
    default_limit = 20
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 1000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('links', OrderedDict([
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link())
            ])),
            ('count', self.count),
            ('limit', self.limit),
            ('offset', self.offset),
            ('results', data)
        ]))


class CursorCustomPagination(pagination.CursorPagination):
    """
    Cursor pagination cho real-time data
    Tốt cho việc thêm/xóa item liên tục
    """
    page_size = 25
    ordering = '-created_at'  # Cần field created_at trong model
    cursor_query_param = 'cursor'
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('links', OrderedDict([
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link())
            ])),
            ('count', len(data)),
            ('results', data)
        ]))
