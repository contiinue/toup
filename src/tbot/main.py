import logging

from aiogram import Bot, Dispatcher, types
from config.settings import TELEGRAM_API_TOKEN
from magic_filter import F
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from api.v1.vacancies import tasks

dp = Dispatcher()

bot = Bot(TELEGRAM_API_TOKEN, parse_mode="HTML")
logger = logging.getLogger(__name__)


class WhoDo(CallbackData, prefix="make"):
    action: str
    value: bool
    notification_id: int
    user_id: int


def _get_link_to_notification(notification_id: int) -> str:
    return f"http://127.0.0.1:8000/{notification_id}"


def get_keyboard(link_to_vacancies: str, notification_id: int, user_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Отправить отклики",
        callback_data=WhoDo(
            action="make",
            value=True,
            notification_id=notification_id,
            user_id=user_id,
        ),
    )
    builder.button(
        text="Посмотреть на сайте",
        callback_data=WhoDo(
            action="make",
            value=False,
            notification_id=notification_id,
            user_id=user_id,
        ),
        url=link_to_vacancies,
    )
    builder.adjust(2)
    return builder.as_markup()


async def send_message_notification(data, user) -> None:
    msg_to_user = (
        f" {user.username}. Собрал вакансии для рассылки, всего вышло: {data.count_vacancies} \n"
        "Что делаем ?"
    )
    await bot.send_message(
        user.telegram_id,
        msg_to_user,
        reply_markup=get_keyboard(
            _get_link_to_notification(data.id_notification),
            data.id_notification,
            user.pk,
        ),
    )


@dp.callback_query(WhoDo.filter(F.action == "make"))
async def callbacks_num_finish_fab(callback: types.CallbackQuery, callback_data: WhoDo):
    if callback_data.value is True:
        await callback.message.edit_text(
            f"Начал рассылку! \n "
            f"Посмотреть вакансии на которые будет отправленно резюме можно тут -\n"
            f"{_get_link_to_notification(callback_data.notification_id)}"
        )
        tasks.make_negotiations.delay(
            callback_data.user_id, callback_data.notification_id
        )
    await callback.answer()


async def send_info_message_negotiations(
    count_valid_negotiations: int, telegram_id: int
):
    msg = f"Завершил Рассылку!. Успешных отправок: {count_valid_negotiations}."
    await bot.send_message(telegram_id, msg)


def main() -> None:
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
