
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser


from packages.models import PackageSettings

from packages.utils import to_hrs
from packages.config import PaymentTypeNumber
from packages.tasks import celery_upload_flat_file


@api_view(["get"])
def upload_term_condition(request):

    terms = {
        "current": ["Default file will saved with md5 as its names."],
        "planning": [
            "File will be saved based on your requirement.",
            "Perment file are to removed "  # cnt
            "within the intervale of %s"  # cnt
            " hrs." % (to_hrs(mins=settings.BM_EXPIRY_TIME_FLAT_FILT_IN_MINS)),  # end
            # 'On reuploading try not to change the file'  # cnt
            # ' name if is it perment file',  # end
            # 'Cancling the upload',
        ],
        "beta": [],
        "warning": [
            "Please remeber once uploaded it is done.",
            "Reuploading cause may unnessary errors for now.",
        ],
        "paytm": [
            "Do not change column's name of paytm, we will take care of the"
            " that one for you."
        ],
    }

    return Response({"detail": terms}, status=status.HTTP_200_OK)


@api_view(["post"])
@parser_classes((FileUploadParser,))
def upload_flat_file(
    request, file_name, file_format=None, use_fields=None, entry_type=2
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

    :return: output of the result form celery
    """

    output = celery_upload_flat_file.delay(request, file_name, file_format, entry_type)

    return output.ready().get(timeout=4)


@api_view(["post"])
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
        use_fields=settings.PAYTM_USE_FILEDS,
        entry_type=PaymentTypeNumber.paytm_type()["id"],
    )
