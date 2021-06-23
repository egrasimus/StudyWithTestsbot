import telebot

bot = telebot.TeleBot(TOKEN)
start = 0
isMeeting = True
isChoose = True
count_of_correct_answer = 0


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я бот для проведения тестирования!\n'
                                      'Давай начнем работать!\n'
                                      'Напиши свое ФИО и группу в следующем формате:\n'
                                      'Иванов Иван Иванович, БСБО-05-19')


@bot.message_handler(content_types=['text'])
def test(message):
    global start
    global count
    global isMeeting
    global isChoose
    global name
    global group
    global tests_name
    global count_of_correct_answer
    global right_answer

    if isMeeting:
        # Запись данных о пользователе
        name = message.text.split(',')[0]
        group = message.text.split(',')[1]
        bot.send_message(message.chat.id, 'Введите название теста, который желаете пройти')
        isMeeting = False

    # Выбор теста
    elif isChoose:
        tests_name = message.text
        try:
            with open(f'{tests_name}.txt', 'r', encoding='UTF-8') as test:
                count = sum(1 for line in test)
            isChoose = False
            keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            bt0 = telebot.types.KeyboardButton('Начать')
            keyboard1.add(bt0)
            bot.send_message(message.chat.id, 'Отлично, теперь нажмите <b>Начать</b>', parse_mode='html',
                             reply_markup=keyboard1)
        except BaseException:
            bot.send_message(message.chat.id, 'Такого теста нет, попробуйте другой')

    # Работа с заданием теста
    elif not isMeeting and not isChoose:
        # Проверка правильности ответа
        if start % 5 == 0 and start != 0:
            if right_answer == message.text:
                count_of_correct_answer += 1
                bot.send_message(message.chat.id, 'Это <b>верный ответ!</b>', parse_mode='html')
            else:
                bot.send_message(message.chat.id,
                                 f'К сожалению <b>ответ не верен</b>, правильным ответом было: {right_answer}',
                                 parse_mode='html')

        # Если это было последнее задание в тесте
        if start == count:
            bot.send_message(message.chat.id, f'Поздравляю, тест решен!\n'
                                              f'Результаты студента {name} из группы {group}:\n'
                                              f'Вы верно ответили на <b>{count_of_correct_answer} из {int(count / 5)}</b>',
                             parse_mode='html')
            isChoose = True
            start = 0
            count_of_correct_answer = 0
            keyboard1 = telebot.types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Введите название следующего теста, который желаете пройти',
                             reply_markup=keyboard1)


        else:
            try:
                with open(f'{tests_name}.txt', 'r', encoding='UTF-8') as test:
                    # Обнуление специальной клавиатуры
                    keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

                    # Пропуск пройденных строк
                    for i in range(start):
                        test.readline()

                    # Обработка 5 следующих строк
                    for i in range(start, start + 5):
                        # Чтение строки
                        line = test.readline()

                        if i == start:
                            bot.send_message(message.chat.id, f'{int(start / 5) + 1}) {line}')
                            bot.send_message(message.chat.id, '<b>Выберите один из перечисленных ответов:</b>',
                                             parse_mode='html')
                        elif i == start + 1:
                            bt1 = telebot.types.KeyboardButton(line[1:-1])
                            bot.send_message(message.chat.id, line[1:-1])
                        elif i == start + 2:
                            bt2 = telebot.types.KeyboardButton(line[1:-1])
                            bot.send_message(message.chat.id, line[1:-1])
                        elif i == start + 3:
                            bt3 = telebot.types.KeyboardButton(line[1:-1])
                            bot.send_message(message.chat.id, line[1:-1])
                        elif i == start + 4:
                            bt4 = telebot.types.KeyboardButton(line[1:-1])
                            bot.send_message(message.chat.id, line[1:-1])

                        # Если это верный ответ
                        if line[0] == '+':
                            right_answer = line[1:-1]

                    # Создание клавиатуры с вариантами ответа
                    keyboard1.add(bt1).add(bt2).add(bt3).add(bt4)
                    bot.send_message(message.chat.id, '<b>Ваш ответ:</b>', reply_markup=keyboard1, parse_mode='html')

                    start += 5
                    test.close()

            except BaseException:
                bot.send_message(message.chat.id, 'Пожалуйста, пользуйтесь специальной клавиатурой')


bot.polling(none_stop=True)