from aiogram import Dispatcher, types


async def echo_message(message: types.Message):
    await message.answer("I received your message!")


def register_handlers(dp: Dispatcher):
    dp.message.register(echo_message)
