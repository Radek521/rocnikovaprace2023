from rest_framework.decorators import api_view
from rest_framework.response import Response
from zaklad.models import Mistnost
from .serializers import MistnostSerializer
from zaklad.api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/mistnosti',
        'GET /api/mistnosti/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms = Mistnost.objects.all()
    serializer = MistnostSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, pk):
    room = Mistnost.objects.get(id=pk)
    serializer = MistnostSerializer(room, many=False)
    return Response(serializer.data)