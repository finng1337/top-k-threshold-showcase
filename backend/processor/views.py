from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Processor
from .algorithms import get_k_naive, get_k_treshold, get_field_index, get_aggr_func
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
        start, elapsedTime = 0, 0

        if fields != []:
            match algorithm:
                case 'naive':
                    allProcessors = list(Processor.objects.filter(type__exact=dataSet))
                    start = time.time()
                    rowsRead, processors = get_k_naive(int(k), allProcessors, fields, get_aggr_func(aggrFunc))
                    elapsedTime = time.time() - start
                case 'treshold':
                    fieldsIndexes = {}
                    for field in fields:
                        fieldName, order = field.rsplit('_', 1)
                        fieldsIndexes[fieldName + '_normalized'] = get_field_index(fieldName, dataSet, order)
                    start = time.time()
                    rowsRead, processors = get_k_treshold(int(k), fieldsIndexes, fields, get_aggr_func(aggrFunc))
                    elapsedTime = time.time() - start
        else:
            serializedProcs = ProcessorSerializer(list(Processor.objects.filter(type__exact=dataSet))[:int(k)], many=True)

            return Response({
                'time': 0,
                'rows_read': 0,
                'data': serializedProcs.data
            }, status=status.HTTP_200_OK)


        serializedProcs = ProcessorSerializer(processors, many=True)

        return Response({
            'time': elapsedTime,
            'rows_read': rowsRead,
            'data': serializedProcs.data
        }, status=status.HTTP_200_OK)