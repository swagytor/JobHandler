ANSWERS = ('1', '2')


def get_user_answer():
    while True:
        user_input = input('Введите команду: ')
        if user_input in ANSWERS:
            return user_input
        print('Неизвестная команда!\n'
              'Повторите попытку\n')


def get_number():
    while True:
        user_input = input('Введите целое положительное число: ')
        if user_input == '':
            return 0
        elif user_input.isdigit() and int(user_input) >= 0:
            return int(user_input)

        print('Вы ввели некорректное значение!\n'
              'Повторите попытку\n')