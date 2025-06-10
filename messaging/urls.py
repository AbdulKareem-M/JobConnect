from django.urls import path
from . import views

urlpatterns = [
    path("inbox/", views.inbox, name="inbox"),
    path("message/<int:message_id>/", views.message_detail, name="message_detail"),
    path("send/<int:receiver_id>/", views.send_message, name="send_message"),
]
