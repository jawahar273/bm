# from django.shortcuts import render

# from rest_framework.views import APIView
# from rest_framework.response import Response


# from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from rest_framework import viewsets
from rest_framework_swagger.views import get_swagger_view

from packages.models import Item, ItemsList
from packages.serializers import ItemSerializer, ItemsListSerializer

# from rest_framework.views import APIView


# Create your views here.
class ItemsListCreateView(viewsets.ModelViewSet):

    serializer_class = ItemsListSerializer
    queryset = ItemsList.objects.order_by('-date')


class ItemCreateView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
