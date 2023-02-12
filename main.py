
import logging
from aiogram import Bot, Dispatcher, executor, types
from translator import get_definition
from googletrans import Translator

API_TOKEN = ""

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
googleTr = Translator()

word_id = ''

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm Translatorbot!\nI can translate from uzbek to english or vice versa.\nType any uzbek or english word.")

@dp.message_handler(commands=['help'])
async def help(message: types.Message):

    await message.answer("Write any words. I will translate it to Uzbek or English. \nTo start over type /start")


@dp.message_handler()
async def tarjimon(message: types.Message):
    msg = message.text
    lang = googleTr.detect(msg).lang
    if len(msg.split()) > 2:
        dest = 'uz' if lang == 'en' else 'en'
        await message.reply(googleTr.translate(msg, dest).text)
    else:
        if lang == 'en':
            word_id = msg
        else:
            word_id = googleTr.translate(msg, 'en').text
        
        lookup = get_definition(word_id=word_id)

        if lookup:
            await message.answer(f"Word: {msg} -- Definitions: {lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply_audio(lookup['audio'])
        else:
            await message.answer("Bunday so'z mavjud emas!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
