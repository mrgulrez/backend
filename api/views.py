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
