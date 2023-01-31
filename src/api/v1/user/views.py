from django.contrib.auth import login
from django.shortcuts import redirect
from rest_framework.views import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet

from user.models import User
from .serializers import UserSerializer
from config.settings import HH_CLIENT_ID
from .utils import get_url_to_grant_access
from .auth_hh import set_user_tokens, update_tokens


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        model = serializer.save()
        login(self.request, model)


class TokenView(ViewSet):
    redirect_uri = f"http://127.0.0.1:8000/api/v1/auth/set_tokens/"

    @action(methods=["get"], detail=False)
    def update_auth_tokens(self, request):
        update_tokens(request.user)

    @action(methods=["get"], detail=False)
    def set_tokens(self, request):
        if request.GET.get("code", False):
            set_user_tokens(request.user, request.GET.get("code"), self.redirect_uri)
            return Response(data={"true": "t"})
        url = get_url_to_grant_access(HH_CLIENT_ID, self.redirect_uri)
        return redirect(url)
