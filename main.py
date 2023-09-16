import os
from time import sleep

# Переменные
cell = "_"
game_field = tuple()  # игровое поле (матрица)
cross_zero = ('X', '0')
answer_yes_tuple = ('yes', 'y', 'да', '+', 'конечно')
answer_no_tuple = ('no', 'n', 'не', 'нет', '-', 'exit')
db_end = {
    "X": "Победил игрок №1!",
    "0": "Победил игрок №2!",
    "_": "У нас Ничья!",
}


def print_field() -> None:
    """Функция выводит в консоль игровое поле"""
    print()
    print('Игровое поле')
    for i in game_field:
        print('-' * 13)
        print(f'| {" | ".join(i)} |', sep="\n")
    print('-' * 13)
    print()


def clear_console() -> None:
    """Функция для очистки консоли от лишнего текста для улучшения визуализации игры."""
    os.system('cls' if os.name == 'nt' else 'clear')


def correct_input(lst: list) -> bool:
    """Функция проверяет корректность ввода координат и возвращает bool значение.
    На входе получаем список и проверяем его по следующим критериям:
    1) Список состоит из 2 элементов;
    2) Все элементы цифры;
    3) Все элементы в интервале от 1 до 3."""
    return len(lst) == 2 and all(map(str.isdigit, lst)) and all(map(lambda x: int(x) in [1, 2, 3], lst))


def free_cell(*args) -> bool:
    """Функция проверяет свободна клетка или нет и возвращает bool значение."""
    x, y = args
    return game_field[x][y] == cell


def end_game(symbol: str) -> str:
    """Функция проверяет, закончилась ли игра или нет."""
    if not any(map(lambda x: cell in x, game_field)):
        result = cell
    elif game_field[0][0] == game_field[0][1] == game_field[0][2] == symbol or \
            game_field[1][0] == game_field[1][1] == game_field[1][2] == symbol or \
            game_field[2][0] == game_field[2][1] == game_field[2][2] == symbol or \
            game_field[0][0] == game_field[1][0] == game_field[2][0] == symbol or \
            game_field[0][1] == game_field[1][1] == game_field[2][1] == symbol or \
            game_field[0][2] == game_field[1][2] == game_field[2][2] == symbol or \
            game_field[0][2] == game_field[1][1] == game_field[2][0] == symbol or \
            game_field[0][0] == game_field[1][1] == game_field[2][2] == symbol:
        result = symbol
    else:
        result = ''
    return result


def next_move(symbol: str) -> None:
    """Функция принимает символ (крестик или нолик, зависит от хода игрока) и запускает следующий алгоритм:
    1) Отображает игровое поле (вызов функции print_field);
    2) Запрашивает у игрока координаты для дальнейшего размещения символа на игровом поле.
    3) Проверяет корректность ввода (вызов функции correct_input);
    4) Проверяет свободна клетка или нет (вызов функции free_cell);
    5) Размещает символ на игровом поле при выполнении условий 3 и 4;
    6) Запускает функцию повторно при невыполнении условий 3 и 4."""
    print()
    print(f'Ход игрока №{cross_zero.index(symbol) + 1}')
    print_field()
    coordinates_field = input(
        f'Введите координаты (от 1 до 3), через пробел, куда хотите поставить {symbol}, например, 1 2\n')

    if correct_input(coordinates_field.split()):
        player_x, player_y = map(lambda x: int(x) - 1,
                                 coordinates_field.split())  # преобразовываем введённые цифры в индексы матрицы

        if free_cell(player_x, player_y):
            game_field[player_x][player_y] = symbol
        else:
            print('Ошибка! Клетка занята. Повторите ввод и введите другие координаты.')
            next_move(symbol)

    else:
        print('Ошибка! Некорректный ввод. Повторите ввод.')
        next_move(symbol)


def game(ind: (int, bool)) -> None:
    """Функция для непосредственного движка игры т.е. поочерёдный ход игроков и запуск проверки завершения игры
    через каждый ход. На входе получаем целое число 0 или 1 (True or False), что подразумевает под собой игрока №1 or 2.
    Также происходит очистка консоли перед каждым ходом через функцию clear_console.
    По завершении игры, предлагается сыграть ещё одну чтобы не перезапускать программу."""

    clear_console()
    symbol = cross_zero[ind]
    next_move(symbol)

    the_end = end_game(symbol)
    if the_end:
        clear_console()
        print_field()
        print(db_end[the_end])

        flag = True
        while flag:
            print()
            answer = input('Желаете сыграть ещё одну игру? Y\\N\n').lower()

            if answer in answer_yes_tuple:
                flag = False
                new_game()
            elif answer in answer_no_tuple:
                print('Всего хорошего!')
                sleep(1)
                flag = False
            else:
                print('Некорректный ввод. Повторите ввод.')
                continue
    else:
        game(not ind)


def new_game() -> None:
    """Функция обновляет матрицу game_field (обнуляет её) и запускает новую игру."""
    sleep(2)

    global game_field
    game_field = [[cell for _ in range(3)] for _ in range(3)]  # игровое поле (матрица)
    game(0)


if __name__ == '__main__':
    print('Добро пожаловать в игру "Крестики - нолики!"')
    new_game()
