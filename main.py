#from time import sleep
import asyncio
from asyncio import sleep
from aiogram.types import ParseMode
import aiogram
import sqlite3
from aiogram import Bot, Dispatcher, types
import random
from aiogram import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
#from aiogram import ParseMode, ReplyKeyboardMarkup, KeyboardButton
import logging
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage= MemoryStorage()
bot = Bot(token="")
dp = Dispatcher(bot, storage=storage)
connect = sqlite3.connect('bd')             #создание бд
c = connect.cursor()
#c.execute('CREATE TABLE users ( id INTEGER PRIMARY KEY, duh integer, friends integer, status integer, inventory integer, strength integer, speed integer, reaction integer, energy integer, travel integer, predel integer, money integer)')
#c.execute('CREATE TABLE sklad ( id INTEGER PRIMARY KEY, name text, quantity integer)')
#c.execute('CREATE TABLE items (id_item integer PRIMARY KEY, name text, description text, class text, bonus integer)')
#my_list = ['menu_kb()', 'citi_kb()', 'movies_kb()', 'friend_kb()', 'setting_kb()']


list = []
class Statess(StatesGroup):
    noduh= State()
    wait = State()
    do = State()
    menu= State()
    battle= State()
    chatt= State()

def menu_kb():

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Город'), KeyboardButton('Действия'), KeyboardButton('Друзья')).add(KeyboardButton('Настройки'), KeyboardButton('Профиль'))
    return kb
def citi_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Рейтинг'), KeyboardButton('Ивенты'), KeyboardButton('Кузня')).add(KeyboardButton('Торговый квартал'), KeyboardButton('Чат'), (KeyboardButton('Работа'))).add(KeyboardButton('Назад'))
    return kb
def movies_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Путешествие'), KeyboardButton('Тренировка'), KeyboardButton('Поглошение енергии')).add(KeyboardButton('Назад'))
    return kb
def friend_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(''), KeyboardButton(''), KeyboardButton('')).add(KeyboardButton(''), KeyboardButton('')).add(
        KeyboardButton('Назад'))
    return kb
def setting_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(''), KeyboardButton(''), KeyboardButton('')).add(KeyboardButton(''), KeyboardButton('')).add(
        KeyboardButton('Назад'))
    return kb
def dange_kb():
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(''), KeyboardButton('')).add(KeyboardButton('Назад'))
    return kb
def fid(fid):
    connect = sqlite3.connect('bd')
    c = connect.cursor()
    c.execute(f'UPDATE users SET predel = strength+ speed+ reaction WHERE id = {fid}')
    connect.commit()
    c.execute(f'SELECT * FROM users WHERE id = {fid}')
    return c.fetchall()
startt = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
startt.add(KeyboardButton('/help'), KeyboardButton('Faq')).add(KeyboardButton('/menu'))


@dp.message_handler(Text(equals='Назад'), state='*')
async def menu(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        dat=data['last']
    if str(await state.get_state())=='Statess:wait':
        async with state.proxy() as data:
            data['last'] = 'menu_kb()'
        await Statess.menu.set()
        await message.answer('Вы вернулись назад', reply_markup=movies_kb())
    elif dat=='menu_kb()':
        await message.answer('Вы вернулись назад', reply_markup=menu_kb())
    elif dat=='citi_kb()':
        async with state.proxy() as data:
            data['last'] = 'menu_kb()'
        await Statess.menu.set()
        await message.answer('Вы вернулись назад', reply_markup=citi_kb())
    elif dat=='movies_kb()':
        async with state.proxy() as data:
            data['last'] = 'menu_kb()'
        await message.answer('Вы вернулись назад', reply_markup=movies_kb())
    elif dat=='friend_kb()':
        async with state.proxy() as data:
            data['last'] = 'menu_kb()'
        await message.answer('Вы вернулись назад', reply_markup=friend_kb())
    elif dat=='setting_kb()':
        async with state.proxy() as data:
            data['last'] = 'menu_kb()'
        await message.answer('Вы вернулись назад', reply_markup=setting_kb())


@dp.message_handler( state=Statess.chatt)
async def menu(message: types.Message):
    if message.from_user.username:
        link = f'https://t.me/{message.from_user.username}'
    else:
        link = ''
    for chat_id in list:
        await bot.delete_message(message.chat.id, message.message_id)
        try:
            await bot.send_message(chat_id, f'[{message.from_user.first_name}]({link}): {message.text}', parse_mode=types.ParseMode.MARKDOWN)
        except Exception as e:
            print(f'Error sending message to chat_id {chat_id}: {e}')


@dp.message_handler(commands='menu')
async def menu(message: types.Message):
    await Statess.menu.set()
    await message.answer('menu', reply_markup=menu_kb())
@dp.message_handler(commands='help')
async def help(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/help'), KeyboardButton('/stats'))
    await bot.send_message(message.chat.id, """/start - ....
/stats - ...""", reply_markup=kb)
    await message.delete()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    # kb.add(help)
    connect = sqlite3.connect('bd')
    c = connect.cursor()
    c.execute(f'SELECT * FROM users WHERE id = {message.chat.id}')
    # c.execute('delete from ctc')
    # c.execute('delete from users')
    # connect.commit()
    fid = c.fetchall()
    print(fid)
    if not fid:
       fid = message.chat.id
       c.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (fid, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100))
       # c.execute('DELETE FROM ctc')
       connect.commit()
    c.execute(f'SELECT * FROM users WHERE id = {message.chat.id}')
    fid = c.fetchall()
    print(fid)
    if fid[0][1]==0:
     #   await Statess.noduh.set()11111111111111111111111111111111111111111111111111111111111111111111111111111
        startt.add(KeyboardButton('Проявить совего духа☀️🌑'))
    await bot.send_message(chat_id=message.chat.id, text="""приветствую тебя message.from_user.first_name, это бот с духами .... По типу тамагочи. 
Faq - информация по боту
Проявить совего духа - случайным образом выдать духа (если его нету) 
ну начало примерно такое)""", reply_markup=startt)



@dp.message_handler(Text(equals='Проявить совего духа☀️🌑'), state=Statess.noduh)
async def duh(message: types.Message):
        duh = InlineKeyboardMarkup(row_width=3)
        i1 = InlineKeyboardButton(text='1', callback_data='1')
        i2 = InlineKeyboardButton(text='2', callback_data='2')
        i3 = InlineKeyboardButton(text='3', callback_data='3')
        duh.add(i1)
        await bot.send_message(chat_id=message.chat.id, text='Вы вошли Храм вечного сияния ', reply_markup=startt)
        ran= random.randint(1, 3)
        if ran == 2:
            duh.add(i2)
            await sleep(60)
        elif ran== 3 :
            duh.add(i2, i3)
            await sleep(120)
        await sleep(60)
        await bot.send_message(chat_id=message.chat.id, text=' духи которых ты заинтересовал', reply_markup=duh)



@dp.message_handler(Text(equals='Меню'))
async def menu(message: types.Message):
    await Statess.menu.set()
    await message.answer('Главное меню', reply_markup=menu_kb())

@dp.message_handler(Text(equals='Город'), state=Statess.menu)#''''''''''''''''''''''''''''''''''''''''''''''''''
async def citi(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'menu_kb()'
    await message.answer('Вы вошли в город', reply_markup=citi_kb())

@dp.message_handler(Text(equals='Рейтинг'), state=Statess.menu)
async def top(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'citi_kb()'
    connect = sqlite3.connect('bd')
    c = connect.cursor()
    # Выполняем SQL-запрос с функцией ORDER BY и LIMIT для получения 10 самых больших значений столбца "column_name" из таблицы "table_name", включая также идентификаторы "id"
    c.execute("SELECT id, predel FROM users ORDER BY predel DESC LIMIT 10")
    # Извлекаем результат запроса
    top = c.fetchall()
    message_text = 'Топ-10 пользователей:\n\n'
    for i, top in enumerate(top, start=1):
        fid, strength = top
        user = await bot.get_chat(fid)
        message_text += f'{i}. {user.first_name}, Сила: {strength}\n'
    top_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    top_kb.add(KeyboardButton('Назад'))
    await message.answer(f'{message_text}', reply_markup=top_kb, parse_mode='HTML')

@dp.message_handler(Text(equals='Ивенты'), state=Statess.menu)
async def ivent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'citi_kb()'
    ivent_kb=ReplyKeyboardMarkup(resize_keyboard=True)
    ivent_kb.add(KeyboardButton('Принять квест'), KeyboardButton('Создать квест')).add(KeyboardButton('Назад'))
    await message.answer('Вы вошли в город', reply_markup=ivent_kb)

@dp.message_handler(Text(equals='Кузня'), state=Statess.menu)
async def dom(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'citi_kb()'
    dom_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    dom_kb.add(KeyboardButton('Оружие'), KeyboardButton('Браня'), KeyboardButton('Сферы')).add(KeyboardButton('Назад'))
    await message.answer('Вы вошли в город', reply_markup=dom_kb)


@dp.message_handler(Text(equals='Торговый квартал'), state=Statess.menu)
async def shop(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'citi_kb()'
    shop_kb=ReplyKeyboardMarkup(resize_keyboard=True)
    shop_kb.add(KeyboardButton('Вернутся')).add(KeyboardButton('Назад'))
    await message.answer('Вы вошли в город', reply_markup=shop_kb)

@dp.message_handler(Text(equals='Чат'), state=Statess.menu)
async def chatt(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last'] = 'citi_kb()'
    await Statess.chatt.set()
    global list
    list.append(message.chat.id)
    chatt_kb=ReplyKeyboardMarkup(resize_keyboard=True)
    chatt_kb.add(KeyboardButton('Назад'))
    await message.answer('Вы вошли в город', reply_markup=chatt_kb)

@dp.message_handler(Text(equals='Работа'), state=Statess.menu)
async def dange(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'menu_kb()'
        data['movie'] = 'Работа'
    await Statess.wait.set()
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('1'), KeyboardButton('3'), KeyboardButton('6')).add(KeyboardButton('Назад'))
    await message.answer('Вы вошли в подземелье', reply_markup=kb)


@dp.message_handler(Text(equals='Действия'), state=Statess.menu)#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
async def movie(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'menu_kb()'
    await message.answer('Выберете дейвтие', reply_markup=movies_kb())

@dp.message_handler(Text(equals='Тренировка'), state=Statess.menu)
async def work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'movies_kb()'
    work_kb=ReplyKeyboardMarkup(resize_keyboard=True)
    work_kb.add(KeyboardButton('Сила'), KeyboardButton('Реакция'), KeyboardButton('Скорость')).add(KeyboardButton('Назад'))
    await message.answer('Вы вошли в город', reply_markup=work_kb)


@dp.message_handler(lambda message: message.text in ['Сила', 'Реакция', 'Скорость', 'Путешествие', 'Поглошение енергии'], state=Statess.menu)
async def d(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Назад'))
    await Statess.wait.set()
    async with state.proxy() as data:
        data['movie'] = message.text
    await message.answer('Напишите сколько времени(часов)', reply_markup=kb)
    print(Statess)


@dp.message_handler(state=Statess.wait)
async def da(message: types.Message, state: FSMContext):
    print('wait')
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Назад'))
    if message.text.isdigit()== True and 0 < int(message.text) < 17:
        connect = sqlite3.connect('bd')
        c = connect.cursor()
    #strength integer, speed integer, reaction integer, energy integer, travel integer)
        async with state.proxy() as data:
            if data['movie']=='Сила':
                move='strength'
            if data['movie']=='Реакция':
                move= 'reaction'
            if data['movie'] == 'Скорость':
                move = 'speed'
            if data['movie'] == 'Путешествие':
                move = 'travel'
            if data['movie'] == 'Поглошение енергии':
                move = 'energy'
            if data['movie'] == 'Работа':
                move = 'money'
                '''await message.answer('теперь вы заняты', reply_markup=kb)
                await Statess.do.set()
                await asyncio.sleep(int(message.text) * 1)
                await Statess.menu.set()
                
                await message.answer(f'вы заработали {random.randint(5, 10)*int(message.text)}', reply_markup=kb)
                c.execute(f'UPDATE users SET {move} = {move}+{j} WHERE id = {message.chat.id}')
                connect.commit()
                return'''



        await message.answer('теперь вы заняты', reply_markup=kb)
        await Statess.do.set()


        j=0
        for i in range(int(message.text)):
            if str(await state.get_state()) == 'Statess:do':
                await asyncio.sleep(2)
                j=i
            else:
                c.execute(f'UPDATE users SET {move} = {move}+{j} WHERE id = {message.chat.id}')
                connect.commit()
                break
        c.execute(f'UPDATE users SET {move} = {move}+{j} WHERE id = {message.chat.id}')
        connect.commit()
        await message.answer('вы закончили', reply_markup=kb)
        await Statess.menu.set()

    else:
        await message.answer('Попробуй ввести число от 1 до 16', reply_markup=kb)
        await Statess.wait.set()
    async with state.proxy() as data:
        data['last'] = 'movies_kb()'
    print(fid(message.chat.id))



@dp.message_handler(Text(equals='Друзья'), state="*")#''''''''''''''''''''''''''''''''''''''''''''
async def friend(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'menu_kb()'
    await message.answer('Ваши друзья', reply_markup=friend_kb())

@dp.message_handler(Text(equals='Профиль'), state="*")#''''''''''''''''''''''''''''''''''''''''
async def profile(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'menu_kb()'
    info=fid(message.chat.id)

    await message.answer(f'''Профиль пользователя
Ник: Лёша
ID: {info[0][0]}

┌ Уровень: 11
├ Опыт: 1105 / 1255
├ Уровень духа: 88
└ Енергия:67/67

┌ 👥 Друзья
└ Количество: {info[0][2]}

┌ 🎈 Инвентарь
└ Предметов: {info[0][4]}''')

@dp.message_handler(Text(equals='Настроики'), state="*")#''''''''''''''''''''''''''''
async def setting(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'menu_kb()'


    await message.answer('Настроики', reply_markup=setting_kb())




@dp.message_handler(Text(equals='Подземелье'), state=Statess.menu)
async def dange(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'citi_kb()'

    await message.answer('Вы вошли в подземелье', reply_markup=dange_kb())

@dp.message_handler(state=Statess.do)
async def menu(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Профиль'), KeyboardButton('Профиль'), KeyboardButton('Чат'), KeyboardButton('Настроики'))
    await message.answer('Главное меню', reply_markup=kb)




@dp.callback_query_handler(lambda c: c.data == '1')
async def cl_start(callback: types.callback_query):
    print(1)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Меню'))
    await bot.edit_message_text(text=' harakteristika', chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)
    await callback.answer('', reply_markup=kb)



if __name__ == '__main__' :
    executor.start_polling(dp, skip_updates=True)