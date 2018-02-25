
import re
import datetime
import os

from django.http import Http404
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser
# from django_filters.rest_framework import DjangoFilterBackend

from packages.models import (Item,
                             ItemsList,
                             MonthBudgetAmount,
                             PackageSettings)
from packages.serializers import (ItemSerializer,
                                  ItemsListSerializer,
                                  ItemsListSerializerOnlyForListFun,
                                  MonthBudgetAmountSerializer,
                                  PackageSettingsSerializer)
# from packages.config import PaymentTypeNumber
from packages.utlity import flatter_list, to_hexdigit, to_hrs


class MonthBudgetAmountView(viewsets.ModelViewSet):
    '''
    All the filter are based on current loged in user.
    :model:`packages.MonthBudgetAmount`

    retrieve:
    Retrive a specifi object based on the month and year as it primary key.

    list:
    Get all the object inside the model.

    update:
    Get the specific object and the udpate field, change the value.

    '''
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
            return Response({'detail': 'Wrong date fomate'},
                            status=status.HTTP_400_BAD_REQUEST)

    def save_or_error_response(self, save_object):
        if not save_object.is_valid():
            return Response({'detail': 'wrong data given'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not save_object.save():
            return Response({'detail': 'unable to save the request data'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(save_object.data)

    def return_only_monthYear(self, month_year=None):
        month_year = month_year.rsplit('-', 1)[0]
        return datetime.datetime.strptime(month_year, "%Y-%m").date()

    def create_or_update_entry(self, custom_request_data, update=None):
        serializers = None
        if update:
            serializers = MonthBudgetAmountSerializer(update,
                                                      data=custom_request_data)
        else:
            serializers = MonthBudgetAmountSerializer(data=custom_request_data)
        return self.save_or_error_response(serializers)

    def retrieve(self, request, month_year=None):

        serializers = self.get_valid_date_or_error_response(month_year)
        if serializers:
            return serializers

        month_year = self.return_only_monthYear(month_year)
        queryset = MonthBudgetAmount.objects.filter(month_year=month_year,
                                                    user=request.user.id)
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


@api_view(['get'])
def get_range_mba(request, start, end=None):
    '''
     both the argument are nessary and pass the month and year with '01' as
     starting date.
     .. deprecated::
        this function is deprecated and will be removed.
    '''

    response = []
    status_code = status.HTTP_200_OK
    # %Y-%m-%d formate checking. 
    regex_date = r'(19|20)\d\d([- /.])(0[1-9]|1[012])\2(0[1-9]|[12][0-9]|3[01])'
    # whole date fomate
    checking_start = re.search(regex_date, start)
    if checking_start and end and re.search(regex_date, end):
        # check based on regex expression
        response = MonthBudgetAmount.objects.filter(date__range=(start, end),
                                                    user=request.user.id)
        serializers = MonthBudgetAmountSerializer(data=response, many=True)
        serializers.is_valid()
        return Response(serializers.data, status=status_code)
    elif checking_start and not end:
        response = {'detail': 'need ranges of date'}
        status_code = status.HTTP_400_BAD_REQUEST
        return Response(serializers.data, status=status_code)
    else:
        response = {'detail': 'Wrong date formate please check it again'}
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
        # self.get_valid_date_or_error_response(month_year)
        request.data.update({'user': request.user.id})

        return self.create_or_update_entry(request.data)

    def update(self, request, pk=None):
        request.data.update({'user': request.user.id})
        return self.create_or_update_entry(request.data, self.get_object())

    def partial_update(self, request, pk=None):
        request.data.update({'user': request.user.id})

        return self.create_or_update_entry(request.data, self.get_object())

    def destroy(self, request, pk=None):
        # request.data.update({'user': request.user.id})
        try:
            to_detete = self.get_object()
            self.perform_destroy(to_detete)

        except Http404:
            Response({'detail': 'content not found'},
                     status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['get'])
def upload_term_condition(request):
    terms = [
        'Default file will not saved',
        'File will be saved based on your requirement',
        ('Perment file are to removed '
         'within the intervale of %d'
         ' hrs' % (to_hrs(settings.EXPIRY_TIME_FLAT_FILT_IN_MINS))),
        ('On reuploading try not to change the file'
         ' name if is it perment file'),
    ]
    return Response({'detail': terms}, status=status.HTTP_200_OK)


@api_view(['post'])
@parser_classes((FileUploadParser,))
def upload_flat_file(request, filename, format=None):
    '''
    Create a MyModel
    ---
    parameters:
        - name: file
          description: file
          required: True
          type: file
    responseMessages:
        - code: 201
          message: Created
    '''
    def upload_file_handler(file_pointer, file_name):
        # file_name = to_hexdigit(file_name)
        with open('%s'(file_name), 'wb') as file:
            for chunk in file_pointer.chunk():
                file.write(chunk)
    import IPython
    IPython.embed()
    access_file = request.FILES['file']
    if len(access_file) <= 0:
        return Response({'details': 'Uploading without file is not allowed'})
    # checking is file to big
    if access_file.multiple_chunks():
        msg = ('Uploaded file is too big'
               ' (%.2f MB).' % (access_file.size / (1000 * 1000)))
        return Response({'detail': msg}, status=status.HTTP_403_FORBIDDEN)


@api_view(['get'])
def get_all_group_in_itemslist(request):
    '''
     get the list of group/catagories items from itemsList object
    '''
    status_code = status.HTTP_200_OK
    response = None
    response = ItemsList.objects.filter(
        user=request.user.id).distinct().values_list('group')
    response = flatter_list(response)
    return Response(response, status=status_code)


class ItemCreateView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


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

    regex_date = r'(19|20)\d\d([- /.])(0[1-9]|1[012])\2(0[1-9]|[12][0-9]|3[01])'
    # whole date fomate
    checking_start = re.search(regex_date, start)

    if checking_start and end and re.search(regex_date, end):
        # check based on regex expression
        response = ItemsList.objects.filter(date__range=(start, end),
                                            user=request.user.id)

        serializers = ItemsListSerializerOnlyForListFun(data=response,
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
def get_currency(request):
    '''
     get the currency symbole and representation from json
    '''
    import json
    file_location = os.path.join(settings.STATIC_ROOT, 'js', '')
    with open(file_location + 'commmon-currency.json') as file:
        return Response(json.loads(file.read()), status=status.HTTP_200_OK)


@api_view(['get', 'put', 'delete'])
def PackageSettingsView(request):

    def save_or_error_response(save_object):
        if not save_object.is_valid():
            return Response({'detail': 'not a valid settings'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not save_object.save():
            return Response({'detail': 'unable to save the request data'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(save_object.data)

    def create_or_update_entry(custom_request_data, update=None):
        serializers = PackageSettingsSerializer(update,
                                                data=custom_request_data)
        return save_or_error_response(serializers)

    if request.method == 'GET':
        queryset = PackageSettings.objects.filter(user__id=request.user.id).values()[0]
        queryset['user'] = queryset.pop('user_id')
        serializers = PackageSettingsSerializer(data=queryset)
        if not serializers.is_valid():
            return Response({'detail': 'setting not found'},
                            status=status.HTTP_404_NOT_FOUND)
        # import json
        # serializers.data['new_settings'] = json.dumps(serializers.data['new_settings'])
        return Response(serializers.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        request.data.update({'user': request.user.id})
        queryset = PackageSettings.objects.filter(user__id=request.user.id).first()#.values()[0]

        return create_or_update_entry(request.data, queryset)

    if request.method == 'DELETE':
        # request.data.update({'user': request.user.id})
        return Response({'detail': 'method is under review'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            to_detete = PackageSettings.objects.filter(user=request.user.id)[0]
            # self.perform_destroy(to_detete)

        except Http404 as e:
            Response({'detail': 'content not found'},
                     status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['get'])
def get_months(request, start, end=None):
    '''
    ... deperated :: in the favour of ItemList view..
    '''
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
    if checking_start and end and re.search(regex_date, end):
        # check based on regex expression
        response = ItemsList.objects.filter(date__range=(start, end),
                                            user_id=request.user.id)
        serializers = ItemsListSerializerOnlyForListFun(data=response,
                                                        many=True)
        serializers.is_valid()
        return Response(serializers.data, status=status_code)
    elif start and not end:
        _date = start.rsplit('-', 1)[0]
        _date = datetime.datetime.strptime(_date, '%Y-%m').date()
        response = ItemsList.objects.filter(date__month=_date.month,
                                            date__year=_date.year,
                                            user_id=request.user.id)
        serializers = ItemsListSerializerOnlyForListFun(data=response,
                                                        many=True)
        serializers.is_valid()
        return Response(serializers.data, status=status_code)
    else:
        response = {'detail': 'Wrong date formate please check it again'}
        status_code = status.HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)
