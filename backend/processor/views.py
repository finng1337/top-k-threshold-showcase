from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .algorithms import get_k_objects
from .serializers import ProcessorSerializer
import time

class ProcessorListView(APIView):
    def get(self, request, *args, **kwargs):
        fields = self.request.query_params.getlist('fields')
        algorithm = self.request.query_params.get('algorithm')
        aggrFunc = self.request.query_params.get('aggr_func')
        k = self.request.query_params.get('k')

        start = time.time()
        rowsRead, processors = get_k_objects(int(k), fields, algorithm, aggrFunc)
        elapsedTime = time.time() - start
        serializedProcs = ProcessorSerializer(processors, many=True)

        return Response({
            'time': elapsedTime,
            'rows_read': rowsRead,
            'data': serializedProcs.data
        }, status=status.HTTP_200_OK)