import contextlib
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

START_TEXT = (
    "👋 *Привет, {name}!*\n"
    "Выбери сайт для просмотра погоды в *Минске*:"
)

def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌤 GISMETEO", url="https://www.gismeteo.ru/weather-minsk-4248/now/"),
                InlineKeyboardButton(text="🗺 YANDEX", url="https://yandex.ru/pogoda/ru/minsk/maps/nowcast?ll=27.5557_53.9027&z=9")
            ],
            [
                InlineKeyboardButton(text="📊 METEO", url="https://meteo.by/minsk/"),
                InlineKeyboardButton(text="🎈 POGODA", url="https://pogoda.by/weather/numerical-weather-2/26851")
            ],
            [
                InlineKeyboardButton(text="ℹ️ О БОТЕ", callback_data="more_info")
            ]
        ]
    )
    return keyboard

def get_back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_to_menu")]
        ]
    )

@router.callback_query(lambda c: c.data == "more_info")
async def about_telegram_bot(callback: CallbackQuery):
    with contextlib.suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text="ℹ️ *Информация о боте*\n\n"
                 "Данный сервис предоставляет быстрый доступ к актуальным "
                 "картам и прогнозам погоды в городе Минске.\n\n"
                 "⚠️ *Писать сюда ничего не нужно — просто нажимайте на кнопки!*",
            parse_mode="Markdown",
            reply_markup=get_back_keyboard()
        )
    await callback.answer()

@router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    with contextlib.suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text=START_TEXT.format(name=callback.from_user.full_name),
            parse_mode="Markdown",
            reply_markup=get_main_inline_keyboard()
        )
    await callback.answer()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        text=START_TEXT.format(name=message.from_user.full_name),
        parse_mode="Markdown",
        reply_markup=get_main_inline_keyboard()
    )

@router.message()
async def default(message: Message):
    with contextlib.suppress(Exception):
        await message.delete()
