from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Receipt
from serializers import ReceiptSerializer
from permissions import ReceiptPermission
# Create your views here.
class ReceiptViewSet(ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [ReceiptPermission]