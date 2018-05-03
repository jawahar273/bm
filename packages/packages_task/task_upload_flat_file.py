import os

from django.conf import settings
from celery.utils.log import get_task_logger

from django.core.cache import cache

from packages.flat_file_interface.api import (FlatFileInterFaceAPI,
                                              FlatFileInterFaceException,
                                              FlatFileInterFaceNotImplemented)
from packages.utlity import to_hexdigit
from packages.models import UploadCount

from bm.taskapp.celery import app

logger = get_task_logger(__name__)


@app.task(bind=True, track_started=True)
def celery_upload_flat_file(self, response, status,
                            request, file_name, file_format,
                            use_fields, entry_type):

    logger.info('Starting the upload file')

    def upload_file_handler(file_pointer, _file_name):
        logger.info('Writing %s to media folder' % (_file_name))

        with open('%s.%s' % (_file_name, file_format), 'wb') as file:

            for chunk in file_pointer.chunks():

                file.write(chunk)

    if file_format not in set(['csv', 'xslx']):

        msg = 'the given file extenstion is not acceptable'
        logger.info('File has is not acceptable')

        return response({'detail': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    access_file = request.FILES['file']

    if len(access_file) <= 0:

        logger.info('File is empty')

        return response({'details': 'Uploading without file is not allowed'})

    # checking is file to big
    if access_file.multiple_chunks():

        logger.info('File has reject due to big size'
                    ' of (%.2f MB).' % (access_file.size / (1000 * 1000)))
        msg = ('Uploaded file is too big'  # cnt
               ' (%.2f MB).' % (access_file.size / (1000 * 1000)))  # end

        return response({'detail': msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    file_location = os.path.join('%s' % (settings.MEDIA_ROOT),
                                 to_hexdigit(file_name))

    upload_file_handler(access_file, file_location)

    try:

        logger.info('Starting the feed file data to Database')
        ffi_api = FlatFileInterFaceAPI(request.user.id)
        ffi_api.read_file(file_format, file_location,
                          usecols=use_fields)
        try:

            ffi_api.mapping_fields(entry_type)

        except FlatFileInterFaceNotImplemented as e:

            logger.error('Database error (Flat File feed)-'
                         ' (selected maybe unwanted options) %s' % e)

            return response({'detail': 'Method not allowed'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        ffi_api.insert_db()
        ffi_api = None
        logger.info('Flat File feed to Database success')

        # UploadCount.objects.cre
        return response({'details': 'success insert to database'},
                        status=status.HTTP_200_OK)

    except FlatFileInterFaceException as e:

        logger.error('Flat File feed to Database error'
                     ' (unknown) %s' % e)

        return response({'detail': 'error in processing file'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

