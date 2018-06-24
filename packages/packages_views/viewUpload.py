
import logging

from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser
from django.core.files.storage import FileSystemStorage

from packages.models import PackageSettings
from packages.config import PaymentTypeNumber
from packages.tasks import celery_upload_flat_file
from bm.users.utils import DotDict
from packages.utils import to_hexdigit

# Get an instance of a logger
logger = logging.getLogger(__name__)


@api_view(["get"])
def upload_term_condition(request):

    terms = {
        "current": [
            "Default file will saved with md5 as its names.",
            "File will be saved on tmp file system.",
        ],
        "planning": [],
        "beta": [],
        "warning": [],
        "paytm": [
            "Do not change column's name of paytm, we will take care of the"
            " that one for you."
        ],
    }

    return Response({"detail": terms}, status=status.HTTP_200_OK)


def upload_file_wrapper(request, temp_location, file_name, file_format):

    def upload_file_handler(file_pointer, _file_name):
        """These file are upload and written to the server.


        :param file_pointer: [python native file pointer]
        :type file_pointer: [object]
        :param _file_name: [file name of the upload folder]
        :type _file_name: [string]

        ChangeLog:
            -- Sunday 24 June 2018 07:08:37 PM IST
            @jawahar273 [Verions 0.1]
            -1- Init Code
        """

        logger.info("Writing %s to media folder" % (_file_name))

        with temp_location.open("%s.%s" % (_file_name, file_format), "wb") as file:

            for chunk in file_pointer.chunks():

                file.write(chunk)

        return Response(
            {"detail": ("File has been uploaded", ". Please for the system to process")}
        )

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

    return upload_file_handler(access_file, to_hexdigit(file_name))


def upload_flat_file(
    request, file_name, file_format=None, use_fields=None, entry_type=None
):
    """
    Upload the file and insert them on the database based
    the flat file interface.

    refer entry type in `packages.config`
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

    temp_location = FileSystemStorage(settings.BM_FILESYSTEMSTORAGE_PATH)

    result = upload_file_wrapper(request, temp_location, file_name, file_format)

    request = DotDict({"user_id": request.user.id})
    _temp_location = DotDict({"base_location": temp_location.base_location})

    output = celery_upload_flat_file.delay(
        request, file_name, file_format, use_fields, entry_type, _temp_location
    )
    output.ready()

    return result


@api_view(["post"])
@parser_classes((FileUploadParser,))
def is_paytm_active(request, file_name, file_format=None):
    """This function is kind of inhertices of the
    :py:func:upload_flat_file (refer parameters)
    which is useful for specific file uploading that is Paytm
    """

    pack_setting = PackageSettings.objects.filter(user_id=request.user.id)
    pack_setting = pack_setting.first()

    if pack_setting.active_paytm == "N":

        return Response(
            {"detail": "paytm uploading is diabled"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
    #  entry type == 1 is equal to paytm

    return upload_flat_file(
        request,
        file_name,
        file_format,
        use_fields=settings.BM_PAYTM_USE_LIST,
        entry_type=PaymentTypeNumber.paytm_type(),
    )
