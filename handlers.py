from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
import asyncio

from db import add_clients, show_clients, delete_client_by_id
router = Router()

def crud_inline_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Добавить')],[KeyboardButton(text='Удалить')],
            [KeyboardButton(text='Показать')]
        ],
        resize_keyboard=True,
    )
    return keyboard


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    await message.answer(
        f"Привет, {user.first_name}! 👋\n"
        "Я бот для учета клиентов.",
        reply_markup=crud_inline_keyboard(),
    )
# Add clients
@router.message(F.text == "Добавить")
async def add_client_menu(message: Message):
    await message.answer(
        "Введите данные клиента через запятую:\n\n"
        "Имя,Телефон,Email"
    )

@router.message(lambda msg: ',' in msg.text)
async def add_client_handler(message: Message):
    try:
        username, phone, email = [
            item.strip()
            for item in message.text.split(",")
        ]

        if len(username) > 20:
            await message.answer(
                "Имя должно быть не длиннее 20 символов."
            )
            return

        if not username.isalpha():
            await message.answer(
                "Имя должно содержать только буквы."
            )
            return

        add_clients(username, phone, email)
        await asyncio.sleep(1)
        await message.answer(
            "✅ Клиент успешно добавлен."
        )
    except ValueError:
        await message.answer(
            "Неверный формат.\n"
            "Пример:\n"
            "Иван,77771234567,ivan@gmail.com"
        )

# Show clients
@router.message(F.text == "Показать")
async def show_client_menu(message: Message):
    clients = show_clients()

    if not clients:
        await message.answer('Клиентов нету!')
        return

    text = 'Список клиентов:\n\n'

    for clients in clients:
        text += (
            f"ID: {clients[0]}\n"
            f"Имя: {clients[1]}\n"
            f"Номер телефона: {clients[2]}\n"
            f"Почта: {clients[3]}\n\n"
        )

    await message.answer(text)

# delete clients
@router.message(F.text == "Удалить")
async def delete_clients_menu(message: Message):
    await message.answer('Если хотите удалить клиента по ID, то воспользуйтесь командой /delete -> номер ID <-')

@router.message(F.text.startswith("/delete"))
async def delete_client_handler(message: Message):
    try:
        client_id = int(message.text.split()[1])

        delete_client_by_id(client_id)

        await message.answer(
            f"✅ Клиент с ID {client_id} удалён."
        )

    except IndexError:
        await message.answer(
            "Укажите ID.\n"
            "Пример: /delete 3"
        )

    except ValueError:
        await message.answer(
            "ID должен быть числом."
        )
