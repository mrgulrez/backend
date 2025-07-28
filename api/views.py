from django.shortcuts import render, redirect
from .models import Message

def landing_page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        text = request.POST.get('text')
        if name and text:
            Message.objects.create(name=name, text=text)
            return redirect('/')  # to prevent resubmission on refresh

    messages = Message.objects.all().order_by('-id')
    return render(request, 'landing.html', {'messages': messages})
