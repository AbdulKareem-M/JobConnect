from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by("-sent_at")
    return render(request, "inbox.html", {"messages": messages})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True
    message.save()
    return render(request, "message_detail.html", {"message": message})

@login_required
def send_message(request, receiver_id):
    if request.method == "POST":
        receiver = get_object_or_404(User, id=receiver_id)
        content = request.POST.get("content")

        if content:
            Message.objects.create(sender=request.user, receiver=receiver, content=content)

            # If the request is AJAX, return JSON response
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": True})

        return redirect("message_detail", message_id=receiver_id)

    return redirect("inbox")
