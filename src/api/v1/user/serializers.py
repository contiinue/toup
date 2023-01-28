from rest_framework import serializers
from user.models import User, AuthHH


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "resume_id",
            "covering_letter",
            "telegram_id",
        )


class AuthHHSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthHH
        fields = ("access_token", "refresh_token")
