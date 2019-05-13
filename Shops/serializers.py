from rest_framework import serializers
from .models import Shops


class ShopSerializer(serializers.ModelSerializer):
    image=serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        fields = (
            'id',
            'name',
            'distance',
            'image',
        )
        model = Shops

