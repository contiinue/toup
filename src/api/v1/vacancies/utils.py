from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from user.models import User


async def _get_user(user_id) -> User | None:
    try:
        return await sync_to_async(User.objects.get)(pk=user_id)
    except ObjectDoesNotExist:
        return None
