from django.urls import path
from . import views

urlpatterns = [
    path("", views.TempMailList.as_view(), name="index"),
    path("gen/", views.GenerateTempMail.as_view(), name="gen"),
    path("messages/<int:id>", views.TempMessagesList.as_view(), name="messages"),
    path("messages_detail/<int:id>/<int:message_id>/", views.TempMessageDetailView.as_view(), name="messages_detail"),
    path("logout/", views.Logout.as_view(), name="logout"),
]
