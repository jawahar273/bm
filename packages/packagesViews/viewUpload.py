import os

from django.conf import settings

from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser

from packages.flat_file_interface.api import (FlatFileInterFaceAPI,
                                              FlatFileInterFaceException,
                                              FlatFileInterFaceNotImplemented)
from packages.utlity import to_hexdigit, to_hrs
from packages.config import PaymentTypeNumber


@api_view(['get'])
def upload_term_condition(request):
    terms = {
        'current': [
            'Default file will saved with md5 as its names.',
        ],
        'planning': [
            'File will be saved based on your requirement.',
            'Perment file are to removed '  # cnt
            'within the intervale of %s'  # cnt
            ' hrs.' % (to_hrs(mins=settings.EXPIRY_TIME_FLAT_FILT_IN_MINS
                              )),  # end
            # 'On reuploading try not to change the file'  # cnt
            # ' name if is it perment file',  # end
            # 'Cancling the upload',
        ],
        'beta': [
        ],
        'warning': [
            'Please remeber once uploaded it is done.',
            'Reuploading cause only unnessary errors.'
        ],
        'paytm': [
            'Do not change column\' name of paytm, we will take care of the'
            ' that one for you.',
        ]
    }
    return Response({'detail': terms}, status=status.HTTP_200_OK)


@api_view(['post'])
@parser_classes((FileUploadParser,))
def upload_flat_file(request, file_name, file_format=None,
                     use_fields=None, entry_type=2):
    '''
    Upload the file and insert them on the database based
    the flat file interface.
    refer entry type in `packages.config`
    '''

    def upload_file_handler(file_pointer, _file_name):
        # file_name = to_hexdigit(file_name)
        with open('%s.%s' % (_file_name, file_format), 'wb') as file:
            for chunk in file_pointer.chunks():
                file.write(chunk)

    if file_format not in set(['csv', 'xslx']):
        msg = 'the given file extenstion is not acceptable'
        return Response({'detail': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    access_file = request.FILES['file']
    if len(access_file) <= 0:
        return Response({'details': 'Uploading without file is not allowed'})

    # checking is file to big
    if access_file.multiple_chunks():
        msg = ('Uploaded file is too big'  # cnt
               ' (%.2f MB).' % (access_file.size / (1000 * 1000)))  # end

        return Response({'detail': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    file_location = os.path.join('%s' % (settings.MEDIA_ROOT),
                                 to_hexdigit(file_name))

    upload_file_handler(access_file, file_location)

    try:
        ffi_api = FlatFileInterFaceAPI()
        ffi_api.read_file(file_format, file_location,
                          usecols=use_fields)
        try:
            ffi_api.mapping_fields(entry_type)
        except FlatFileInterFaceNotImplemented as e:
            return Response({'detail': e},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        ffi_api.insert_db(request.user.id)
        ffi_api = None
        return Response({'details': 'success insert to database'},
                        status=status.HTTP_200_OK)

    except FlatFileInterFaceException:
        return Response({'detail': 'error in processing file'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['post'])
def is_paytm_active(request, file_name, file_format=None):
    pack_setting = PackageSettings.objects.filter(user_id=request.user.id).first()
    if pack_setting.active_paytm == 'N':
        return Response({'detail': 'paytm uploading is diabled'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #  entry type == 1 is equal to paytm
    return upload_flat_file(request, file_name,
                            file_format,
                            use_fields=settings.PAYTM_USE_FILEDS,
                            entry_type=PaymentTypeNumber.paytm_type()['id'])


