from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    """
    Custom pagination for the REST API. The current page & total number of pages are returned to aid front-end
    pagination
    """
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'current': self.page.number,
            'page_count': self.page.paginator.num_pages,
            'results': data
        })