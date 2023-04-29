from rest_framework import serializers
from .models import Processor

class ProcessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processor
        fields = [
            'pk',
            'name',
            'cores',
            'cores_normalized',
            'threads',
            'threads_normalized',
            'frequency',
            'frequency_normalized',
            'boost_frequency',
            'boost_frequency_normalized',
            'cache',
            'cache_normalized',
            'lithography',
            'lithography_normalized',
            'tdp',
            'tdp_normalized',
        ]