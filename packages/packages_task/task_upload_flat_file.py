import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from celery.utils.log import get_task_logger
from rest_framework.response import Response
from rest_framework import status

from packages.flat_file_interface.api import (
    FlatFileInterFaceAPI,
    FlatFileInterFaceException,
    FlatFileInterFaceNotImplemented,
)
from packages.utils import to_hexdigit
from bm.taskapp.celery import app

logger = get_task_logger(__name__)


@app.task(bind=True, track_started=True)
def celery_upload_flat_file(
    self, request, file_name, file_format, use_fields, entry_type
):
    """Uploading the flat file is done in async with
    the help of 3rd party libary `Celery`.

    :param request: [Request object form view djagno]
    :type request: [request]
    :param file_name: [name of the file in uploading]
    :type file_name: [str]
    :param file_format: [flat file extention]
    :type file_format: [str]
    :param use_fields: [This is useful for find which columns are allowed]
    :type use_fields: [list]
    :param entry_type: [Mark to find upload type like (patym, user's etc)]
    :type entry_type: [int]
    """
    logger.info("Starting the upload file")

    temp_location = FileSystemStorage("/tmp")

    def upload_file_handler(file_pointer, _file_name):
        """These file are upload and written to the server.


        :param file_pointer: [python native file pointer]
        :type file_pointer: [object]
        :param _file_name: [file name of the upload folder]
        :type _file_name: [string]
        """
        logger.info("Writing %s to media folder" % (_file_name))
        print("start3")
        import IPython

        IPython.embed()
        with temp_location.open("%s.%s" % (_file_name, file_format), "wb") as file:

            for chunk in file_pointer.chunks():

                file.write(chunk)

    # checking the file extention
    if file_format not in set(["csv", "xslx"]):

        msg = "the given file extenstion is not acceptable"
        logger.info("File has is not acceptable")

        return Response({"detail": msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    access_file = request.FILES["file"]

    # checking the file is empty or not
    if len(access_file) <= 0:

        logger.info("File is empty")

        return Response({"details": "Uploading without file is not allowed"})

    # checking is file to big
    if access_file.multiple_chunks():

        logger.info(
            "File has reject due to big size"
            " of (%.2f MB)." % (access_file.size / (1000 * 1000))
        )
        msg = "Uploaded file is too big" " (%.2f MB)." % (  # cnt
            access_file.size / (1000 * 1000)
        )  # end

        return Response({"detail": msg}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # NEED OPTIMIATION:
    print("start2")
    import IPython

    IPython.embed()
    file_location = os.path.join(
        temp_location.base_location, "%s.%s" % (to_hexdigit(file_name), file_format)
    )

    upload_file_handler(access_file, to_hexdigit(file_name))

    try:

        logger.info("Starting the feed file data to Database")
        ffi_api = FlatFileInterFaceAPI(request.user.id)
        ffi_api.read_file(file_format, file_location, usecols=use_fields)
        try:

            ffi_api.mapping_fields(entry_type)

        except FlatFileInterFaceNotImplemented as e:

            logger.error(
                "Database error (Flat File feed)-"
                " (selected maybe unwanted options) %s" % e
            )

            return Response(
                {"detail": "Method not allowed"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        ffi_api.insert_db()
        ffi_api = None
        logger.info("Flat File feed to Database success")

        # UploadCount.objects.cre
        return Response(
            {"details": "success insert to database"}, status=status.HTTP_200_OK
        )

    except FlatFileInterFaceException as e:

        logger.error("Flat File feed to Database error" " (unknown) %s" % e)

        return Response(
            {"detail": "error in processing file"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
