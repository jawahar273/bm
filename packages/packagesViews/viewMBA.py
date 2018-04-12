import re
import datetime


from django.conf import settings

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view


from packages.models import MonthBudgetAmount
from packages.serializers import MonthBudgetAmountSerializer


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
    serializer_class = MonthBudgetAmountSerializer
    filter_fields = ('budget_amount',)
    # filter_backends = (DjangoFilterBackend)

    def get_queryset(self):

        return MonthBudgetAmount.objects.filter(user=self.request.user.id)

    def get_valid_date_or_error_response(self, month_year=None):
        '''Chech the date is a valid based on the application's
        standards.

        :param str month_year: the date from the user.
        :rtype: JSON
        '''

        regex_date = settings.BM_REGEX_DATE_FORMAT

        if not re.search(regex_date, month_year):

            return Response({'detail': 'Wrong date fomate'},
                            status=status.HTTP_400_BAD_REQUEST)

    def save_or_error_response(self, save_object):

        if not save_object.is_valid():
            import IPython
            IPython.embed()

            return Response({'detail': 'wrong data given'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not save_object.save():

            return Response({'detail': 'unable to save the request data'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(save_object.data, status=status.HTTP_200_OK)

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
            import IPython
            IPython.embed()
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

        return Response(serializers.data, status=status.HTTP_200_OK)

    def create(self, request):

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
    regex_date = settings.BM_REGEX_DATE_FORMAT
    # regex_date = r'(19|20)\d\d([- /.])(0[1-9]|1[012])\2(0[1-9]|[12][0-9]|3[01])'
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
