# from django.shortcuts import render

# from rest_framework.views import APIView
from rest_framework.response import Response


# from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route

from packages.models import Item, ItemsList
from packages.serializers import ItemSerializer, ItemsListSerializer

# from rest_framework.views import APIView

from IPython import embed


# Create your views here.
class ItemsListCreateView(viewsets.ModelViewSet):

    serializer_class = ItemsListSerializer
    queryset = ItemsList.objects.order_by('-date')

    # def list(request, data, **kwargs):
    #     '''
    #        @deprated
    #        get the list of the items
    #     '''
    #     response = {'status_code': 403, 'detail': 'method not allowed'}
    #     # embed()
    #     return Response(response, headers=headers, status=403)

    @list_route()
    def run(self, request):
        return Response({'jfkd': '394'})



class ItemCreateView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

