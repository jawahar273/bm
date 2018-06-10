import datetime
from typing import Dict

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.template import loader

# from django.http import HttpResponse
from celery.utils.log import get_task_logger
from weasyprint import HTML

from bm.taskapp.celery import app
from bm.users.models import User
from bm.users.utils import to_datetime_format, set_cache
from packages.utils import sending_mail_pdf
from packages.models import PackageSettings, ItemsList

logger = get_task_logger(__name__)


@app.task(bind=True, track_started=True)
def celery_generate_summary(self, request, content: Dict) -> None:
    """Generating the summary based on the seleted value
    dashboard from the server.

    ChangLog:
        -- Friday 08 June 2018 11:32:07 PM IST
        @jawahar273 [Version 0.1]
        -3- Logic bug fix on itemlist model.
    """

    logger.info("Initi of parsing of pdf")
    start = content["start"]
    end = content["end"]
    file_name = settings.BM_PDF_FILE_NAME
    file_name += to_datetime_format(
        datetime.datetime.now(), settings.BM_ISO_8601_TIMESTAMP
    )

    file_extention = "pdf"

    _user = User.objects.get(id=request.user.id)
    user_id = _user.id

    load_template = loader.get_template("%s" % (settings.BM_PDF_TEMPLATE_NAME))

    items_list = ItemsList.objects.filter(
        user=user_id, date__range=(start, end)
    ).values()

    html = HTML(
        string=load_template.render(
            {
                "pdf_list": items_list,
                "date_format": settings.BM_STANDARD_DATE_TEMPLATE,
                "pdf_title": settings.BM_PDF_TITLE,
                "pdf_description": settings.BM_PDF_DESCRIPTION,
                "currency_code": PackageSettings.get(user=user_id).currency_details,
            }
        )
    )

    logger.info("parsering  of html to %s " % (file_extention))
    html.write_pdf(target="/tmp/%s.%a" % (file_name, file_extention))

    logger.info("writing of the %s" % (file_extention))

    fs = FileSystemStorage("/tmp")

    try:

        with fs.open("%s.%s" % (file_name, file_extention)) as file_pointer:

            # making a mail woule better options
            logger.info("Perparing for sending mail")

            sending_mail_pdf([_user.email], file_pointer)

            logger.info("Mail has been sended")

    except FileNotFoundError:

        logger.error("unexpected error in founding error")
