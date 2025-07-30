# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import Message
# import json

# @csrf_exempt
# def messages_view(request):
#     if request.method == "GET":
#         messages = list(Message.objects.all().order_by('-id').values())
#         return JsonResponse(messages, safe=False)
    
#     elif request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             name = data.get("name")
#             text = data.get("text")
#             if name and text:
#                 Message.objects.create(name=name, text=text)
#                 return JsonResponse({"status": "success"}, status=201)
#             return JsonResponse({"error": "Name and text required"}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON"}, status=400)
        



# from rest_framework import generics, status
# from rest_framework.response import Response
# from .models import Build
# from .serializers import BuildSerializer, BuildIdSerializer
# import uuid

# class BuildListCreateView(generics.GenericAPIView):
#     queryset = Build.objects.all()

#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return BuildIdSerializer
#         return BuildSerializer

#     def get(self, request, *args, **kwargs):
#         builds = self.get_queryset()
#         serializer = self.get_serializer(builds, many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         build_id = str(uuid.uuid4())
#         data = request.data.copy()
#         data['build_id'] = build_id
#         serializer = BuildSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class BuildDetailView(generics.GenericAPIView):
#     queryset = Build.objects.all()
#     serializer_class = BuildSerializer
#     lookup_field = 'build_id'
#     def get(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import uuid
from .models import Message, Build, DeliveryDetails
from .serializers import (
    MessageSerializer,
    BuildSerializer,
    BuildDetailSerializer,
    DeliveryDetailsSerializer
)

# Message Endpoints
@api_view(['GET', 'POST'])
def message_list(request):
    if request.method == 'GET':
        messages = Message.objects.all().order_by('-id')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def message_detail(request, pk):
    try:
        message = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageSerializer(message)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        partial = (request.method == 'PATCH')
        serializer = MessageSerializer(message, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Build Endpoints
@api_view(['GET', 'POST'])
def build_list(request):
    if request.method == 'GET':
        builds = Build.objects.all().order_by('-created_at')
        serializer = BuildSerializer(builds, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data.copy()
        data['build_id'] = str(uuid.uuid4())
        serializer = BuildSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def build_detail(request, build_id):
    try:
        build = Build.objects.get(build_id=build_id)
    except Build.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BuildDetailSerializer(build)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        data = request.data.copy()
        partial = (request.method == 'PATCH')
        serializer = BuildSerializer(build, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        build.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def set_delivery(request, build_id):
    try:
        build = Build.objects.get(build_id=build_id)
    except Build.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['delivery_id'] = str(uuid.uuid4())
    data['build'] = build.id
    serializer = DeliveryDetailsSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delivery Endpoints
@api_view(['GET', 'POST'])
def delivery_list(request):
    if request.method == 'GET':
        deliveries = DeliveryDetails.objects.all().order_by('-created_at')
        serializer = DeliveryDetailsSerializer(deliveries, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data.copy()
        data['delivery_id'] = str(uuid.uuid4())
        serializer = DeliveryDetailsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def delivery_detail(request, delivery_id):
    try:
        delivery = DeliveryDetails.objects.get(delivery_id=delivery_id)
    except DeliveryDetails.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DeliveryDetailsSerializer(delivery)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        data = request.data.copy()
        partial = (request.method == 'PATCH')
        serializer = DeliveryDetailsSerializer(delivery, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        delivery.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)