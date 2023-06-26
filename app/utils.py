ANSWERS = ('1', '2')


def get_user_answer() -> str:
    """
    Проводит проверку правильности ответа пользователя
    :return: ответ пользователя
    """
    while True:
        user_input = input('Введите команду: ')

        if user_input in ANSWERS:
            return user_input.lower()

        print('Неизвестная команда!\n'
              'Повторите попытку\n')


def get_number() -> int:
    """
    Проверка числа на корректность
    :return: число пользователя
    """

    while True:
        user_input = input('Введите целое положительное число: ')

        if user_input == '':
            return 0

        elif user_input.isdigit() and int(user_input) >= 0:
            return int(user_input)

        print('Вы ввели некорректное значение!\n'
              'Повторите попытку\n')
