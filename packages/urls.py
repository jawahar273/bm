from django.conf.urls import url

from rest_framework import routers


from packages.views import (
    ItemsListCreateView,
    # ItemCreateView,
    MonthBudgetAmountView,
    PackageSettingsView,
    itemlist_get_by_months,
    get_range_mba,
    get_timezone_list,
    get_all_group_in_itemslist,
    get_currency,
    upload_term_condition,
    is_paytm_active,
    upload_flat_file,
    delete_bulk,
    print_summary,
    print_summary_key,
)


router = routers.DefaultRouter()
router.register("itemslist", ItemsListCreateView, base_name="itemslist")
router.register("mba", MonthBudgetAmountView, base_name="mba")

regex_date_valid = r"[0-9\-]{10}"

app_name = "packages"
urlpatterns = [
    url(r"^settings/", PackageSettingsView, name="package_settings"),
    url(
        r"^itemslist/(?P<start>{})/(?P<end>{})/$".format(
            regex_date_valid, regex_date_valid
        ),
        itemlist_get_by_months,
        name="itemslist_get_by_month",
    ),
    url(
        r"^get_group_items/(?P<start>{})/(?P<end>{})/$".format(
            regex_date_valid, regex_date_valid
        ),
        get_all_group_in_itemslist,
        name="get_group_list",
    ),
    url(r"^timezone_list/$", get_timezone_list, name="get_timezone_list"),
    url(
        r"^mba/(?P<start>{})/(?P<end>{})/$".format(regex_date_valid, regex_date_valid),
        get_range_mba,
        name="range_mba",
    ),
    url(r"^currency/$", get_currency, name="currency"),
    url(
        r"^upload-term-condition/$", upload_term_condition, name="upload_term_condition"
    ),
    url(
        r"^paytm-upload/(?P<file_name>[^/]+).(?P<file_format>csv|xslx)/$",
        is_paytm_active,
        name="patym_upload_file",
    ),
    url(
        r"^upload/(?P<file_name>[^/]+).(?P<file_format>csv|xslx)/$",
        upload_flat_file,
        name="upload_file",
    ),
    url(r"^delete-bulk/", delete_bulk, name="delete_bulk"),
    url(
        r"^print-summary/(?P<key_value>[a-z_]{10,20})/$",
        print_summary,
        name="print_summary",
    ),
    url(r"^print-summary-key/$", print_summary_key, name="print_summary_key"),
]

urlpatterns.extend(router.urls)
