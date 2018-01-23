# from django.shortcuts import render

# from rest_framework.views import APIView
import re
import datetime

from rest_framework.response import Response

# from rest_framework.generics import RetrieveUpdateDestroyAPIView,ListCreateAPIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route, api_view
from django_filters.rest_framework import DjangoFilterBackend
from packages.models import Item, ItemsList, MonthBudgetAmount
from packages.serializers import ItemSerializer, ItemsListSerializer, ItemsListSerializerOnlyForListFun, MonthBudgetAmountSerializer

# from rest_framework.views import APIView

from IPython import embed

class MonthBudgetAmountView(viewsets.ModelViewSet):
    lookup_field = 'month_year'
    # queryset =  MonthBudgetAmount.objects.all()#.filter(month_year__month=today.month, month_year__year=today.year)
    # today = datetime.date.today()
    serializer_class = MonthBudgetAmountSerializer
    filter_fields = ('budget_amount',)
    # filter_backends = (DjangoFilterBackend)
    def get_queryset(self):
        return MonthBudgetAmount.objects.filter(user_id=self.request.user.id)

    def retrieve(self, request, month_year=None):
        # embed()
        regex_date = r'(19|20)\d\d([- /.])(0[1-9]|1[012])\2(0[1-9]|[12][0-9]|3[01])'

        if not re.search(regex_date, month_year):
            return Response({'detail': 'Wrong date fomate'}, status=status.HTTP_400_BAD_REQUEST)
        month_year = month_year.rsplit('-', 1)[0]
        month_year = datetime.datetime.strptime(month_year, "%Y-%m").date()
        queryset = MonthBudgetAmount.objects.filter(month_year = month_year, user_id=request.user.id)
        serializers = MonthBudgetAmountSerializer(data=queryset, many=True)
        serializers.is_valid()
        return Response(serializers.data)

    # def get_queryset(self):
    #     embed()
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
       response = MonthBudgetAmount.objects.filter(date__range=(start, end), user_id=request.user.id)
       serializers = MonthBudgetAmountSerializer(data=response, many=True)
       serializers.is_valid()
       return Response(serializers.data, status=status_code)
    elif checking_start and not end:
        # _date = start.rsplit('-', 1)[0]
        # _date = datetime.datetime.strptime(_date, '%Y-%m').date()
        # # embed()
        # response = MonthBudgetAmount.objects.filter(date__month = _date.month, date__year = _date.year, )
        # serializers = MonthBudgetAmountSerializer(data=response, many=True)
        # serializers.is_valid()
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
        return ItemsList.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self, *args, **kwargs):
        serializer_class = None
        if self.action == 'list':
            serializer_class = ItemsListSerializerOnlyForListFun
            # embed()
        else:
            serializer_class = ItemsListSerializer
        return serializer_class

    # def update_amount(self):
    #     if ('post', 'put', 'patch') in self.action.lower():
    #         ItemsList



class ItemCreateView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


@api_view(['get'])
def get_months(request, start, end=None):
    embed()
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
       response = ItemsList.objects.filter(date__range=(start, end), user_id=request.user.id)
       serializers = ItemsListSerializerOnlyForListFun(data=response, many=True)
       serializers.is_valid()
       return Response(serializers.data, status=status_code)
    elif start and not end:
        _date = start.rsplit('-', 1)[0]
        _date = datetime.datetime.strptime(_date, '%Y-%m').date()
        # embed()
        response = ItemsList.objects.filter(date__month = _date.month, date__year = _date.year, user_id=request.user.id)
        serializers = ItemsListSerializerOnlyForListFun(data=response, many=True)
        serializers.is_valid()
        return Response(serializers.data, status=status_code)
    else:
        response = { 'detail': 'Wrong date formate please check it again'}
        status_code = status.HTTP_400_BAD_REQUEST 
        return Response(response, status=status_code)