# from django.shortcuts import render

# from rest_framework.views import APIView
from rest_framework.response import Response


# from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route

from packages.models import Item, ItemsList
from packages.serializers import ItemSerializer, ItemsListSerializer, ItemsListSerializerOnlyForListFun

# from rest_framework.views import APIView

from IPython import embed


# Create your views here.
class ItemsListCreateView(viewsets.ModelViewSet):

    queryset = ItemsList.objects.all()

    # def list(request, data, **kwargs):
    #     '''
    #        @deprated
    #        get the list of the items
    #     '''
    #     response = {'status_code': 403, 'detail': 'method not allowed'}
    #     # embed()
    #     return Response(response, headers=headers, status=403)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            # embed()
            serializer_class = ItemsListSerializerOnlyForListFun
        else:
            serializer_class = ItemsListSerializer
        return serializer_class

    # def update_amount(self):
    #     if ('post', 'put', 'patch') in self.action.lower():
    #         ItemsList



class ItemCreateView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

