# from django.shortcuts import render

# from rest_framework.views import APIView
import re
import datetime

from django.http import Http404

from rest_framework.response import Response

# from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route, api_view
from django_filters.rest_framework import DjangoFilterBackend

from packages.models import Item, ItemsList, MonthBudgetAmount
from packages.serializers import ItemSerializer, ItemsListSerializer, ItemsListSerializerOnlyForListFun, MonthBudgetAmountSerializer

# from rest_framework.views import APIView



class MonthBudgetAmountView(viewsets.ModelViewSet):
    lookup_field = 'month_year'
    # queryset =  MonthBudgetAmount.objects.all()#.filter(month_year__month=today.month, month_year__year=today.year)
    # today = datetime.date.today()
    serializer_class = MonthBudgetAmountSerializer
    filter_fields = ('budget_amount',)
    # filter_backends = (DjangoFilterBackend)
    def get_queryset(self):
        return MonthBudgetAmount.objects.filter(user=self.request.user.id)

    def get_valid_date_or_error_response(self, month_year=None):

        regex_date = r'(19|20)\d\d([- /.])(0[1-9]|1[012])\2(0[1-9]|[12][0-9]|3[01])'

        if not re.search(regex_date, month_year):
            return Response({'detail': 'Wrong date fomate'}, status=status.HTTP_400_BAD_REQUEST)

    def save_or_error_response(self, save_object):
        if not save_object.is_valid():
            return Response({'detail': 'wrong data given'}, status=status.HTTP_400_BAD_REQUEST)

        if not save_object.save():
            return Response({'detail': 'unable to save the requeset data'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(save_object.data)

    def return_only_monthYear(self, month_year=None):
        month_year = month_year.rsplit('-', 1)[0]
        return datetime.datetime.strptime(month_year, "%Y-%m").date()
    
    def create_or_update_entry(self, custom_request_data, update=None):
        serializers = None
        if update:
           serializers = MonthBudgetAmountSerializer(update, data=custom_request_data)
        else:
           serializers = MonthBudgetAmountSerializer(data=custom_request_data)
        return self.save_or_error_response(serializers)

    def retrieve(self, request, month_year=None):

        serializers = self.get_valid_date_or_error_response(month_year)
        if serializers:
            return serializers

        month_year = self.return_only_monthYear(month_year)
        queryset = MonthBudgetAmount.objects.filter(month_year = month_year, user=request.user.id)
        serializers = MonthBudgetAmountSerializer(data=queryset, many=True)
        serializers.is_valid()
        return Response(serializers.data)

    def create(self, request):
        # self.get_valid_date_or_error_response(month_year)
        request.data.update({'user': request.user.id})

        return self.create_or_update_entry(request.data)

    def update(self, request, month_year=None):

        serializers = self.get_valid_date_or_error_response(month_year)
        if serializers:
            return serializers

        request.data.update({'user': request.user.id})
        request.data.update({'month_year': month_year})      
        return self.create_or_update_entry(request.data, self.get_object())


    def partial_update(self, request, month_year=None):
        
        serializers = self.get_valid_date_or_error_response(month_year)
        if serializers:
            return serializers
        request.data.update({'user': request.user.id})

        return self.create_or_update_entry(request.data, self.get_object())


    # def destroy(self, request, month_year=None):
    #     get_valid_date_or_error_response(month_year)

    #     return Response(serializers.data)


    # def get_queryset(self):
    #     queryset = MonthBudgetAmount.objects.all()
    #     # airline = self.request.query_params.get('airline')
    #     _budget_amount = self.request.query_params.get('budget_amount')

    #     if _budget_amount and self.action =='retrieve':
    #         queryset = queryset.filter(workspace_id=workspace, budget_amount=_budget_amount)
    #     elif airline:
    #         queryset = queryset.filter(workspace__airline_id=airline)

    #     return queryset

@api_view(['get'])
def get_range_mba(request, start, end=None):
    '''
     both the argument are nessary and pass the month and year with '01' as 
     starting date.
    '''
    response = []
    status_code = status.HTTP_200_OK
    # %Y-%m-%d formate checking. 
    regex_date = r'(19|20)\d\d([- /.])(0[1-9]|1[012])\2(0[1-9]|[12][0-9]|3[01])'
    # whole date fomate
    checking_start = re.search(regex_date, start)
    if checking_start and end and re.search(regex_date, end) : # check based on regex expression
       response = MonthBudgetAmount.objects.filter(date__range=(start, end), user=request.user.id)
       serializers = MonthBudgetAmountSerializer(data=response, many=True)
       serializers.is_valid()
       return Response(serializers.data, status=status_code)
    elif checking_start and not end:
        response = { 'detail': 'need ranges of date'}
        status_code = status.HTTP_400_BAD_REQUEST 
        return Response(serializers.data, status=status_code)
    else:
        response = { 'detail': 'Wrong date formate please check it again'}
        status_code = status.HTTP_400_BAD_REQUEST 
        return Response(response, status=status_code)  

class ItemsListCreateView(viewsets.ModelViewSet):

    # queryset = ItemsList.objects.all()
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
            return Response({'detail': 'wrong data given'}, status=status.HTTP_400_BAD_REQUEST)

        if not save_object.save():
            return Response({'detail': 'unable to save the requeset data'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(save_object.data)

    def create_or_update_entry(self, custom_request_data):
        serializers = ItemsListSerializer(data=custom_request_data)
        return self.save_or_error_response(serializers)

    def create(self, request):
        # self.get_valid_date_or_error_response(month_year)
        request.data.update({'user': request.user.id})

        return self.create_or_update_entry(request.data)

    def update(self, request, pk=None):
        request.data.update({'user': request.user.id})

        return self.create_or_update_entry(request.data)

    def partial_update(self, request, pk=None):
        request.data.update({'user': request.user.id})

        return self.create_or_update_entry(request.data)

    def destroy(self, request, pk=None):
        # request.data.update({'user': request.user.id})
        try:
            to_detete = self.get_object()
            self.perform_destroy(to_detete)

        except Http404 as e:
            Response({'detail': 'content not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemCreateView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


@api_view(['get'])
def get_months(request, start, end=None):
    response = []
    status_code = status.HTTP_200_OK
    # %Y-%m-%d formate checking. 

    # if len(start) == 7:
    #     regex_date = r'(19|20)\d\d([-])(0[1-9]|1[012])'
    #     checking_start = re.search(regex_date, start)
    # else:
    regex_date = r'(19|20)\d\d([- /.])(0[1-9]|1[012])\2(0[1-9]|[12][0-9]|3[01])'
    # whole date fomate
    checking_start = re.search(regex_date, start)
    if checking_start and end and re.search(regex_date, end) : # check based on regex expression
       response = ItemsList.objects.filter(date__range=(start, end), user=request.user.id)
       serializers = ItemsListSerializerOnlyForListFun(data=response, many=True)
       serializers.is_valid()
       return Response(serializers.data, status=status_code)
    elif start and not end:
        _date = start.rsplit('-', 1)[0]
        _date = datetime.datetime.strptime(_date, '%Y-%m').date()
        response = ItemsList.objects.filter(date__month = _date.month, date__year = _date.year, user=request.user.id)
        serializers = ItemsListSerializerOnlyForListFun(data=response, many=True)
        serializers.is_valid()
        return Response(serializers.data, status=status_code)
    else:
        response = { 'detail': 'Wrong date formate please check it again'}
        status_code = status.HTTP_400_BAD_REQUEST 
        return Response(response, status=status_code)