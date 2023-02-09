from rest_framework import serializers

from models.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    valid_requests = serializers.IntegerField(required=False)
    invalid_requests = serializers.IntegerField(required=False)

    class Meta:
        model = Notification
        fields = (
            "pk",
            "user",
            "date_create",
            "request_notification",
            "vacancies",
            "valid_requests",
            "invalid_requests",
        )
