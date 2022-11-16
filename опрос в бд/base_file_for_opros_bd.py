# Задача взята с фриланса для портфолио
import asyncio
from aiogram import Bot, Dispatcher, types, executor
import logging
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import TOKEN
import sql_for_opros_bd

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher(bot)
ADMIN_ID = '5051821733'
# сектор кнопок(мне лень было создавать отдельный файл!)
first_questionnaire = InlineKeyboardMarkup(2)
first_button1 = InlineKeyboardButton(text="H2o", callback_data='h2o')
first_button2 = InlineKeyboardButton(text="Co2", callback_data='co2')
first_questionnaire.add(first_button1, first_button2)

second_questionnaire = InlineKeyboardMarkup(3)
second_button1 = InlineKeyboardButton(text="Подушка", callback_data='Pillow')
second_button2 = InlineKeyboardButton(text="Ошибка", callback_data='Mistake')
second_button3 = InlineKeyboardButton(text="Стакан", callback_data='Glass')
second_button4 = InlineKeyboardButton(text="Ратакан", callback_data='Ratakan')
second_questionnaire.add(second_button1, second_button2, second_button3, second_button4)


async def on_startup(_):
    await sql_for_opros_bd.db_conn()
    print('БД ПОДКЛЮЧЕНА!')


@dp.message_handler(content_types=["new_chat_members"])
async def new_user(message: types.Message):
    await sql_for_opros_bd.new_user(user_id=message.from_user.id)
    await sql_for_opros_bd.new_user_name(user_name=message.from_user.first_name)


@dp.message_handler(commands=['start'])
async def questionnaire(message: types.Message):
    await sql_for_opros_bd.zero_count(user_id=message.from_user.id)
    await message.answer('СУПЕР-ПУПЕР ОПРОСИК!')
    await message.answer('Обнуление!')
    await asyncio.sleep(2)
    await message.answer('Ты знаешь формулу воды?', reply_markup=first_questionnaire)


# Каллбэки
@dp.callback_query_handler(text='h2o')
async def h2o_answer(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Как переводится ERROR?', reply_markup=second_questionnaire)
    await sql_for_opros_bd.update_count(user_id=callback.from_user.id)


@dp.callback_query_handler(text='co2')
async def h2o_answer(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Как переводится ERROR?', reply_markup=second_questionnaire)


@dp.callback_query_handler(text='Pillow')
async def h2o_answer(callback: types.CallbackQuery):
    result = await sql_for_opros_bd.sel_count(user_id=callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(f"Готово, ты набрал: {result}")


@dp.callback_query_handler(text='Mistake')
async def h2o_answer(callback: types.CallbackQuery):
    await sql_for_opros_bd.update_count(user_id=callback.from_user.id)
    result = await sql_for_opros_bd.sel_count(user_id=callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(f"Готово, ты набрал: {list(result)[0]}")


@dp.callback_query_handler(text='Glass')
async def h2o_answer(callback: types.CallbackQuery):
    result = await sql_for_opros_bd.sel_count(user_id=callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(f"Готово, ты набрал: {result}")


@dp.callback_query_handler(text='Ratakan')
async def h2o_answer(callback: types.CallbackQuery):
    result = await sql_for_opros_bd.sel_count(user_id=callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(f"Готово, ты набрал: {result}")


# точка входа
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)