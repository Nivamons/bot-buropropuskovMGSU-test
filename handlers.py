from aiogram import types, F, Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from middlewares import Red_docx, Docx_to_pdf

class DataEntry(StatesGroup):
    choosing_date = State()
    choosing_name = State()
    choosing_number_auto = State()

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")

@router.message(Command("pass"))
async def entry_date(msg: Message, state: FSMContext):
    await msg.answer("На какую дату хотите заказать пропуск? (например, 19 августа 2023)")
    await state.set_state(DataEntry.choosing_date)

@router.message(DataEntry.choosing_date)
async def entry_name(msg: Message, state: FSMContext):
    await state.update_data(chosen_date = msg.text)
    await msg.answer("На кого заказываете пропуск (ФИО)")
    await state.set_state(DataEntry.choosing_name)

@router.message(DataEntry.choosing_name)
async def entry_number_auto(msg: Message, state: FSMContext):
    await state.update_data(chosen_name = msg.text)
    await msg.answer("Напишите номер машины полностью, (М 011 ВА 777)")
    await state.set_state(DataEntry.choosing_number_auto)

@router.message(DataEntry.choosing_number_auto)
async def complete_chose(msg: Message, state: FSMContext):
    user_data = await state.get_data()
    await msg.answer(f"Вам нужен пропуск для машины {msg.text},"
                     f"водитель: {user_data['chosen_name']},"
                     f"дата: {user_data['chosen_date']}")
    title_file: str = Red_docx("file_load/Пробник.docx",
                               user_data['chosen_date'], msg.text, user_data['chosen_name'])
    out_file: str = Docx_to_pdf(title_file)

    doc = FSInputFile(path=out_file, filename='test.pdf')
    await msg.reply_document(document=doc)
    await state.clear()

@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")