from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import NotificationSerializer
from .models import Notification
# Create your views here.

class NotificationViewsets(ModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    @action(detail=True , methods=["post"])
    def mark_read(self , request , pk = None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields = ["is_read"])

        return Response({ "message" :  "Notification marked as read"})

    @action(detail=True , methods=["post"])
    def mark_all_read(self , request):
        self.get_queryset().filter(is_read = False).update(is_read = True)

        return Response({"message" : "All notifications are marked as read"})