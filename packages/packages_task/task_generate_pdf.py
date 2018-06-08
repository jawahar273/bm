import datetime

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.template import loader

# from django.http import HttpResponse
from celery.utils.log import get_task_logger
from weasyprint import HTML

from packages.models import PackageSettings, ItemsList

from bm.taskapp.celery import app
from bm.users.utils import to_datetime_format, set_cache

logger = get_task_logger(__name__)


@app.task(bind=True, track_started=True)
def celery_generate_summary(self, request):
    """Generating the summary based on the seleted value
    dashboard from the server.

    """

    logger.info("Initi of parsing of pdf")

    file_name = settings.BM_PDF_FILE_NAME
    file_name += to_datetime_format(
        datetime.datetime.now(), settings.BM_ISO_8601_TIMESTAMP
    )

    user_id = request.user.id
    load_template = loader.get_template("%s" % (settings.BM_PDF_TEMPLATE_NAME))

    items_list = ItemsList.objects.filter(user=user_id).values()

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

    logger.info("parsering  of html to pdf")
    html.write_pdf(target="/tmp/%s.pdf" % (file_name))

    logger.info("writing of the pdf")

    fs = FileSystemStorage("/tmp")
    try:

        with fs.open("%s.pdf" % (file_name)) as pdf:

            headers = {}
            headers["Content-Disposition"] = 'inline; filename="%s.pdf"' % (file_name)
            headers["Content-Type"] = "application/pdf"

            # making a mail woule better options
            logger.info("Perparing for sending mail")

    except FileNotFoundError:

        logger.error("unexpected error in founding error")
