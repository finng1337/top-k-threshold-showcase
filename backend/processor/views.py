from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .algorithms import get_k_objects
import time

class ProcessorListView(APIView):
    def get(self, request, *args, **kwargs):
        fields = self.request.query_params.getlist('fields')
        algorithm = self.request.query_params.get('algorithm')
        aggrFunc = self.request.query_params.get('aggr_func')

        start = time.time()
        rowsRead, serializedProcs = get_k_objects(2, fields, algorithm, aggrFunc)
        elapsedTime = time.time() - start

        return Response({
            'time': elapsedTime,
            'rows_read': rowsRead,
            'data': serializedProcs
        }, status=status.HTTP_200_OK)