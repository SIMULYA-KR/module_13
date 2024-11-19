from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = "*****"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = ReplyKeyboardMarkup()
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.add(button2)


@dp.message_handler(text='привет')
async def start(message):
    await message.answer(f'Привет! Я бот помогающий Вашему здоровью.\n'
                         "Введите команду /start, чтобы начать общение")


@dp.message_handler(text="/start")
async def all_messages(message):
    print(f'Чтобы начать, нажмите "Рассчитать"')
    await message.answer(f'Чтобы начать, нажмите "Рассчитать"', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f'Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f'Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    calories_men = 10 * weight + 6.25 * growth - 5 * age + 5
    calories_women = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer('Расчёт произведён, посмотрите информацию')

    @dp.message_handler(text='Информация')
    async def inform(message):
        await message.answer(f'Ваш возраст:  {age}\nВаш рост:      {growth}\nВаш вес:          {weight}\n'
                             f'Ваша норма калорий: {calories_men}, для мужчин\n    '
                             f'                                      {calories_women}, для женщин')

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)