import re
import datetime

from django.conf import settings
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view


from packages.models import Item, ItemsList
from packages.serializers import (ItemSerializer,
                                  ItemsListSerializer,
                                  ItemsListSerializerOnlyForListFun)
from packages.utlity import flatter_list


class ItemsListCreateView(viewsets.ModelViewSet):
    '''Get the ItemsListModel value.
    .. Notes::
        overriding of `list` is handle in get_serializer_class.

    '''

    def get_queryset(self):

        return ItemsList.objects.filter(user=self.request.user.id)

    def get_serializer_class(self, *args, **kwargs):

        serializer_class = None

        if self.action == 'list':
            serializer_class = ItemsListSerializerOnlyForListFun
        else:
            serializer_class = ItemsListSerializer
        return serializer_class

    def save_or_error_response(self, save_object):

        if not save_object.is_valid():
            return Response({'detail': 'wrong data given'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not save_object.save():
            return Response({'detail': 'unable to save the request data'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(save_object.data)

    def create_or_update_entry(self, custom_request_data, update=None):

        serializers = None

        if update:
            serializers = ItemsListSerializer(update,
                                              data=custom_request_data)
        else:
            serializers = ItemsListSerializer(data=custom_request_data)

        return self.save_or_error_response(serializers)

    def create(self, request):

        request.data.update({'user': request.user.id})

        return self.create_or_update_entry(request.data)

    def update(self, request, pk=None):

        request.data.update({'user': request.user.id})
        return self.create_or_update_entry(request.data, self.get_object())

    def partial_update(self, request, pk=None):

        request.data.update({'user': request.user.id})

        return self.create_or_update_entry(request.data, self.get_object())

    def destroy(self, request, pk=None):

        try:
            to_detete = self.get_object()
            self.perform_destroy(to_detete)

        except Http404:
            Response({'detail': 'content not found'},
                     status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemCreateView(viewsets.ModelViewSet):

    serializer_class = ItemSerializer
    queryset = Item.objects.all()


@api_view(['get'])
def get_months(request, start, end=None):
    '''
    ... deperated :: in the favour of ItemList view..
    '''

    response = []
    status_code = status.HTTP_200_OK
    # %Y-%m-%d formate checking. 
    regex_date = settings.BM_REGEX_DATE_FORMAT
    # regex_date = r'(19|20)\d\d([- /.])(0[1-9]|1[012])\2(0[1-9]|[12][0-9]|3[01])'
    # whole date fomate
    checking_start = re.search(regex_date, start)

    if checking_start and end and re.search(regex_date, end):
        # check based on regex expression
        _queryset = ItemsList.objects.filter(date__range=(start, end),
                                             user_id=request.user.id)
        serializers = ItemsListSerializerOnlyForListFun(data=_queryset,
                                                        many=True)
        serializers.is_valid()

        return Response(serializers.data, status=status_code)

    elif start and not end:
        _date = start.rsplit('-', 1)[0]
        _date = datetime.datetime.strptime(_date, '%Y-%m').date()
        _queryset = ItemsList.objects.filter(date__month=_date.month,
                                             date__year=_date.year,
                                             user_id=request.user.id)
        serializers = ItemsListSerializerOnlyForListFun(data=_queryset,
                                                        many=True)
        serializers.is_valid()

        return Response(serializers.data, status=status_code)

    else:
        response = {'detail': 'Wrong date formate please check it again'}
        status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=status_code)


@api_view(['get'])
def itemlist_get_by_months(request, start, end):
    '''
     get the list of items based on the month from starting and ending.
     Extenstion for
     ItemsList object.
     old-method-name: get_months
    '''

    response = []
    # %Y-%m-%d formate checking.
    regex_date = settings.BM_REGEX_DATE_FORMAT
    # regex_date = r'(19|20)\d\d([- /.])(0[1-9]|1[012])\2(0[1-9]|[12][0-9]|3[01])'
    # whole date fomate
    checking_start = re.search(regex_date, start)

    if checking_start and end and re.search(regex_date, end):
        # check based on regex expression
        _queryset = ItemsList.objects.filter(date__range=(start, end),
                                             user=request.user.id)

        serializers = ItemsListSerializerOnlyForListFun(data=_queryset,
                                                        many=True)
        serializers.is_valid()
        status_code = status.HTTP_200_OK

        return Response(serializers.data, status=status_code)

    elif checking_start and not end:
        response = {'detail': 'Need both date ranges'}
        status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=status_code)

    else:
        response = {'detail': 'Wrong date formate please check it again'}
        status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=status_code)


@api_view(['get'])
def get_all_group_in_itemslist(request):
    '''
     get the list of group/catagories items from itemsList object
    '''

    status_code = status.HTTP_200_OK
    _queryset = ItemsList.objects.filter(
         user=request.user.id).values_list('group').order_by('group').distinct()
    _queryset = flatter_list(_queryset)

    return Response(_queryset, status=status_code)
