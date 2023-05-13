from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Processor, RealProcessor
from .algorithms import get_k_naive, get_k_threshold, get_aggr_func
from .serializers import ProcessorSerializer
import time

class ProcessorListView(APIView):
    def get(self, request, *args, **kwargs):
        fields = self.request.query_params.getlist('fields')
        dataSet = self.request.query_params.get('data')
        algorithm = self.request.query_params.get('algorithm')
        aggrFunc = self.request.query_params.get('aggr_func')
        k = self.request.query_params.get('k')

        rowsRead, processors = 0, []

        if dataSet == 'real':
            data = list(RealProcessor.objects.all())
        else:
            data = list(Processor.objects.all())

        start = time.time()
        if fields:
            match algorithm:
                case 'naive':
                    rowsRead, processors = get_k_naive(int(k), data, fields, get_aggr_func(aggrFunc))
                case 'threshold':
                    rowsRead, processors = get_k_threshold(int(k), data, fields, get_aggr_func(aggrFunc))
        else:
            processors = data[:int(k)]

        elapsedTime = time.time() - start

        if dataSet == 'experiment':
            processors = []

        serializedProcs = ProcessorSerializer(processors, many=True)
        return Response({
            'time': elapsedTime,
            'rows_read': rowsRead,
            'data': serializedProcs.data
        }, status=status.HTTP_200_OK)