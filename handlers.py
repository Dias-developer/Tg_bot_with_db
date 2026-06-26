from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart


from state.state import AddClient, DeleteClient
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
        "Я бот для учета клиентов.\n"
        "Если хотите взаимодействовать с ботом, то воспользуйтесь меню!",
        reply_markup=crud_inline_keyboard(),
    )

# Add clients
@router.message(F.text == "Добавить")
async def add_client_menu(message: Message, state: FSMContext):
    await state.set_state(AddClient.waiting_for_username)
    await message.answer('Введите имя клиента:')

@router.message(AddClient.waiting_for_username)
async def add_client_username(message: Message, state: FSMContext):
   username = message.text.strip()

   if len(username) > 20:
       await message.answer('Слишком длинное имя!')
       return

   if not username.isalpha():
       await message.answer("Имя должно содержать только буквы!")
       return

   await state.update_data(username=username)

   await state.set_state(AddClient.waiting_for_phone)

   await message.answer('Введите номер телефона:')


@router.message(AddClient.waiting_for_phone)
async def add_client_phone(message: Message, state: FSMContext):
    phone = message.text.strip()

    if not phone.replace("+", "").isdigit():
        await message.answer(
            "Телефон должен содержать только цифры и +"
        )
        return

    if len(phone) < 11:
        await message.answer('Номер телефона должно содержать 10 цифр!')
        return

    await state.update_data(phone=phone)

    await state.set_state(AddClient.waiting_for_email)

    await message.answer("Введите email:")

@router.message(AddClient.waiting_for_email)
async def add_client_email(message: Message, state: FSMContext):
    email = message.text.strip()

    if '@' not in email or '.' not in email:
        await message.answer(
            "Введите корректный email."
        )
        return

    await state.update_data(email=email)

    data = await state.get_data()

    add_clients(
        data["username"],
        data["phone"],
        data["email"]
    )

    await state.clear()
    await message.answer("✅ Клиент успешно добавлен.")
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
async def delete_clients_menu(message: Message, state: FSMContext):
    await state.set_state(DeleteClient.waiting_for_id)

    await message.answer(
        "Введите ID клиента:"
    )

@router.message(DeleteClient.waiting_for_id)
async def delete_client_handler(message: Message, state: FSMContext):
    client_id = message.text.strip()

    if not client_id.isdigit():
        await message.answer("ID должен быть числом!")
        return

    client_id = int(client_id)

    delete_client_by_id(client_id)

    await state.clear()

    await message.answer(
        f"✅ Клиент с ID {client_id} удалён."
    )