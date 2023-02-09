from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import User


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


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token
