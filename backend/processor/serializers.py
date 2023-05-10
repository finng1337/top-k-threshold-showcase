from rest_framework import serializers
from .models import RealProcessor

class ProcessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealProcessor
        fields = [
            'pk',
            'name',
            'cores',
            'threads',
            'frequency',
            'boost_frequency',
            'cache',
            'lithography',
            'tdp',
        ]