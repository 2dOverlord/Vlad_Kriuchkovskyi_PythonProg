from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import TRANSACTION
from rest_framework import routers, serializers, viewsets, generics, filters
from .serializers import TRANSACTIONSerializer
import django_filters


class TRANSACTIONViewSet(viewsets.ModelViewSet):
    """
    Viewset made for our user.
    """

    serializer_class = TRANSACTIONSerializer
    queryset = TRANSACTION.objects.all()
    lookup_field = "id"
    http_method_names = ["get", "put", "post", "delete"]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = "__all__"

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # if not "count" in response.data.keys():
        #     count = len(response.data)
        #     data = {
        #         'transactions': response.data,
        #         'count': count
        #     }
        #     response.data = data
        # else:
        #     response.data = response.data['results']

        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response:
            data = {
                'status': 200,
                'message': "Transaction has been successfully created.",
            }
            return Response(data, status=status.HTTP_200_OK, headers=response.headers)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        response = super().update(request, *args, **kwargs)
        if response:
            data = {
                'status': 200,
                'message': "Transaction has been successfully updated.",
                'transaction': response.data,
            }
            return Response(data, status=status.HTTP_200_OK, headers=response.headers)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response:
            data = {
                'status': 200,
                'message': "Transaction has been successfully deleted.",
            }
            return Response(data, status=status.HTTP_200_OK, headers=response.headers)
