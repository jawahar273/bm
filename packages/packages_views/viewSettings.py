from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


from packages.models import PackageSettings
from packages.serializers import PackageSettingsSerializer


@api_view(["get", "put", "delete"])
def PackageSettingsView(request):

    def save_or_error_response(save_object):

        if not save_object.is_valid():
            return Response(
                {"detail": "not a valid settings"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not save_object.save():

            return Response(
                {"detail": "unable to save the request data"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(save_object.data)

    def create_or_update_entry(custom_request_data, update=None):

        serializers = PackageSettingsSerializer(update, data=custom_request_data)

        return save_or_error_response(serializers)

    if request.method == "GET":

        queryset = PackageSettings.objects.filter(user__id=request.user.id)
        queryset = queryset.values()[0]
        queryset["user"] = queryset.pop("user_id")
        serializers = PackageSettingsSerializer(data=queryset)

        if not serializers.is_valid():

            return Response(
                {"detail": "setting not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(serializers.data, status=status.HTTP_200_OK)

    if request.method == "PUT":

        request.data.update({"user": request.user.id})
        queryset = PackageSettings.objects.filter(user__id=request.user.id)
        queryset = queryset.first()

        return create_or_update_entry(request.data, queryset)

    if request.method == "DELETE":

        return Response(
            {"detail": "method is not allowed"}, status=status.HTTP_403_FORBIDDEN
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
