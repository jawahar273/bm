import os

from celery.utils.log import get_task_logger

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
    self, request, file_name, file_format, use_fields, entry_type, temp_location
):
    """Uploading the flat file is done in async with
    the help of 3rd party libary `Celery`.

    :param request: [passing custom dict `DotDict`]
    :type request: [DotDict]
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

    # NEED OPTIMIATION:
    file_location = os.path.join(
        temp_location, "%s.%s" % (to_hexdigit(file_name), file_format)
    )

    try:

        logger.info("Starting the feed file data to Database")
        # pasing user id.
        ffi_api = FlatFileInterFaceAPI(request.user_id)
        ffi_api.read_file(file_format, file_location, usecols=use_fields)

        try:

            ffi_api.mapping_fields(entry_type)

        except FlatFileInterFaceNotImplemented as e:

            logger.error(
                "Database error (Flat File feed)-"
                " (selected maybe unwanted options) %s" % e
            )

        ffi_api.insert_db()

        ffi_api = None
        logger.info("Flat File feed to Database success")

    except FlatFileInterFaceException as e:

        logger.error("Flat File feed to Database error" " (unknown) %s" % e)
