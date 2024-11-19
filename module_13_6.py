kb.add(button1)
kb.add(button2)
kb2.add(button3)


@dp.message_handler(commands='start')
async def start(message):
    await message.answer(f'Привет! Я бот помогающий Вашему здоровью.\n'
                         f'Чтобы начать, введите "Рассчитать"')


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Выберите опцию:', reply_markup=kb)


@dp.callback_query_handler(text='formulas')
async def info(call):
    await call.message.answer(f'10 * вес(кг) + 6.25 * рост(см) - 5 '  f'* возраст(лет) + 5 для мужчин\n10 * '
                              f'вес(кг) + 6.25 * рост(см) - 5 * ' f'возраст(лет) - 161 для женщин',
                              reply_markup=kb)
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
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

    await message.answer('Расчёт произведён, посмотрите информацию', reply_markup=kb2)

    @dp.message_handler(text='Информация')
    async def inform(message):
        await message.answer(f'Ваш возраст:  {age}\nВаш рост:      {growth}\nВаш вес:          {weight}\n'
                             f'Ваша норма калорий: {calories_men}, для мужчин\n    '
                             f'{calories_women}, для женщин')

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


