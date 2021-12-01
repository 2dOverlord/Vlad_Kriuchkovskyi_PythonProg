from .models import TRANSACTION
from rest_framework import routers, serializers, viewsets


class TRANSACTIONSerializer(serializers.ModelSerializer):
    class Meta:
        model = TRANSACTION
        fields = "__all__"
        read_only_fields = ('id',)
