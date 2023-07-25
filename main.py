import datetime
from time import sleep
import logging
import asyncio
import openai
from sqlalchemy import insert
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from sqlalchemy.exc import IntegrityError
from aiogram.types.bot_command import BotCommand
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from conf import BOT_TOKEN, WEB_APP_URL, OPEN_API_TOKEN
from models import User, Characters
from storage import SessionLocal, Base, engine

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.WARNING)

Base.metadata.create_all(engine)


# open AI request
async def conversation_with_ai(user_message, character_description):
    openai.api_key = OPEN_API_TOKEN
    prompt = f'Instructions: You are {character_description}.' \
             f' In answer you must use language same as user. ' \
             f'Give only full answer! ' \
             f'Do not give dangerous information! ' \
             f' message: {user_message}'

    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1000)
    answer = response['choices'][0]['text']

    return answer.strip()


# bot commands
async def set_commands():
    commands = [
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/menu", description="Сменить персонажа"),

    ]
    await bot.set_my_commands(commands)


# handler /start
@dp.message_handler(commands=['start'])
async def handle_start(message: Message):
    # takes user information
    user = message.from_user

    user_data = {
        "user_id": user.id,
        "username": user.username,
        "name": user.first_name,
        "surname": user.last_name,
        "time": datetime.datetime.now()
    }

    # create db session
    db = SessionLocal()

    # create query with user info and try to insert into db
    query = insert(User).values(**user_data)
    try:
        db.execute(query)
        db.commit()

    except IntegrityError:
        pass
    except Exception:
        db.rollback()
        await message.reply("Произошла ошибка. Повторите позже.")
    finally:
        db.close()

    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="Выбери персонажа", url=WEB_APP_URL + "?user_id=" + str(user.id)))

    await bot.send_message(message["from"]["id"],
                           f"Привет! По ссылке ниже выбери с каким героем ты хочешь пообщаться сегодня!",
                           reply_markup=keyboard)

    while True:
        sleep(5)
        db = SessionLocal()
        user = db.query(User).filter(User.user_id == user_data["user_id"]).first()
        if not user.character:
            db.close()
            continue
        else:
            char = db.query(Characters).filter(Characters.id == user.character).first()
            await bot.send_message(message["from"]["id"], f"Привет! Меня зовут {char.name}! О чем хочешь поговорить?")
            db.close()
            break


# handler text messages
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: Message):
    user_id = message.from_user.id
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    char_id = user.character

    if not char_id:
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Выбери персонажа", url=WEB_APP_URL + "?user_id=" + str(user_id)))
        await bot.send_message(message["from"]["id"], f"Чтобы начать общение, нужно выбрать персонажа.", reply_markup=keyboard)

    char = db.query(Characters).filter(Characters.id==user.character).first()

    user_message = message.text
    new_message = await conversation_with_ai(user_message, char.open_ai_description)
    await bot.send_message(message["from"]["id"], new_message)


# handler /menu
@dp.message_handler(commands=['menu'])
async def handle_menu(message: Message):
    user_id = message.from_user.id
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="Выбери персонажа", url=WEB_APP_URL + "?user_id=" + str(user_id)))

    await bot.send_message(message["from"]["id"],
                           f"Привет! По ссылке ниже выбери с каким героем ты хочешь пообщаться сегодня!",
                           reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    asyncio.run(set_commands())
