from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Processor
from .serializers import ProcessorSerializer

class ProcessorListView(APIView):
    def get(self, request, *args, **kwargs):
        processors = Processor.objects.all()
        serializer = ProcessorSerializer(processors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)