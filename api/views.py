from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Message
import json

@csrf_exempt
def messages_view(request):
    if request.method == "GET":
        messages = list(Message.objects.all().order_by('-id').values())
        return JsonResponse(messages, safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            text = data.get("text")
            if name and text:
                Message.objects.create(name=name, text=text)
                return JsonResponse({"status": "success"}, status=201)
            return JsonResponse({"error": "Name and text required"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        


        
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Build
from .serializers import BuildSerializer, BuildIdSerializer
import uuid

class BuildListCreateView(generics.GenericAPIView):
    queryset = Build.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BuildIdSerializer
        return BuildSerializer

    def get(self, request, *args, **kwargs):
        builds = self.get_queryset()
        serializer = self.get_serializer(builds, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        build_id = str(uuid.uuid4())
        data = request.data.copy()
        data['build_id'] = build_id
        serializer = BuildSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BuildDetailView(generics.GenericAPIView):
    queryset = Build.objects.all()
    serializer_class = BuildSerializer
    lookup_field = 'build_id'
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)