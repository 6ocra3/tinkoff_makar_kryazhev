import random
import time
import copy
import colorama

colorama.init()


class Ceil:
    """Класс для обозначения одной клетки"""

    def __init__(self, is_alive, neighbours=None):
        """Принимает переменную is_alive (1 - клетка живая, 0 - нет) и создает переменную neighbours"""
        self.is_alive = is_alive
        self.neighbours = neighbours

    def __str__(self):
        """Выводит '=' если is_alive = 0 (клетка мертвая) и '#' если is_alive = 1 (клетка живая)"""
        return ["=", "#"][self.is_alive]

    def rebirth(self):
        """Функция для определения значения is_alive в следующем поколении"""
        if self.neighbours <= 1 or self.neighbours > 3:
            self.is_alive = 0
        elif not self.is_alive and self.neighbours == 3:
            self.is_alive = 1

    def __eq__(self, other):
        """
        Переопределение функции сравнения. Назовем экземпляры класса Ceil равными если равны их значения is_alive
        """
        if self.is_alive == other.is_alive:
            return True
        return False


class Space:
    """Класс для нашего мира(вселенной)"""

    def __init__(self, input_type):

        if input_type == '1':

            print("Введите через проблем размер вертикали матрицы и  размер горизонтали матрицы соответсвенно")
            self.y, self.x = map(int, input().split())
            # Создание и заполнение двумерного массива, случайными экземплярами Ceil, индексация от 1 до
            # self.y/self.x + 1 для успешной реализации метода field_exp()
            self.field = [[0] * (self.x + 2) for i in range((self.y + 2))]
            for i in range(1, self.y + 1):
                for j in range(1, self.x + 1):
                    self.field[i][j] = Ceil(int(random.choices([0, 1], weights=[2, 1])[0]))
            self.field_exp()
            # Удаление системных сообщений
            self.clear_pre_verse(4)
            print(self)

        else:
            print(
                'Введите матрицу состояющую из "=" и "#", где "#" - живая клетка, "-" - неживая, "/" - окончание ввода')
            arr = list()
            k = input()
            while k != '/':
                arr.append(list(k))
                k = input()
            self.x = len(arr[0])
            self.y = len(arr)
            self.field = [[0] * (self.x + 2) for i in range(self.y + 2)]
            # Создание и заполнение двумерного массив экземплярами Ceil на основе введеной пользователем матрицы
            # Индексация от 1 до self.y/self.x + 1  также для реализации метода field_exp
            for i in range(1, self.y + 1):
                for j in range(1, self.x + 1):
                    self.field[i][j] = Ceil(int(arr[i - 1][j - 1] == "#"))
            self.field_exp()
            self.clear_pre_verse(self.y + 4)
            print(self)
        # Переменная для  последующего хранения двумерной копии нашей матрицы
        self.pre_field = None

    def next_gen(self):
        """
        Метод для генерации следующего поколения. Последовательно выполняются фукнция neighbours, копирование
        текущей матрицы, применения метода rebirth у каждого экземпляра Ceil
        """
        self.neighbours()
        # Создание копии двумерного массива
        self.pre_field = copy.deepcopy(self.field)
        for i in range(1, self.y + 1):
            for j in range(1, self.x + 1):
                self.field[i][j].rebirth()

    def field_exp(self):
        """Метод для расширения нашей матрицы на одну строчку/столбец по всем сторонам (реализация бесконечного поля).
        Эти новые строки/столбцы мы заполняем крайними элементами с противоположной стороны,
        угловые элементы заполняются 'мертвыми' экземплярами Ceil """
        # Я решил, что реализовать данный метод легче и безопаснее чем вводить множество проверок/исключений для
        # крайних элементов матрицы в методе neighbours()

        # Заполнение угловых элементов
        self.field[0][0] = Ceil(0, 0)
        self.field[0][self.x + 1] = Ceil(0, 0)
        self.field[self.y + 1][self.x + 1] = Ceil(0, 0)
        self.field[self.y + 1][0] = Ceil(0, 0)
        # Заполнение дополнительной строки сверху и снизу
        self.field[0][1: -1] = self.field[-2][1:-1]
        self.field[-1][1:-1] = self.field[1][1:-1]
        # Заполнение дополнительного столбца слева и справа
        for i in range(1, self.y + 1):
            self.field[i][0] = self.field[i][-2]
            self.field[i][-1] = self.field[i][1]

    def neighbours(self):
        """Метод для подсчета количества соседей для каждого элемента"""
        for i in range(1, self.y + 1):
            for j in range(1, self.x + 1):
                cnt = 0
                for vert in [-1, 0, 1]:
                    for hor in [-1, 0, 1]:
                        if vert != 0 or hor != 0:
                            # Увеличение счетчика соседей если is_alive соседнего экземпляра Ceil равен 1
                            cnt += self.field[i + vert][j + hor].is_alive
                self.field[i][j].neighbours = cnt

    def __str__(self, clear=True):
        """
        Переопределение метода str для класса Space, выведение двумерного массива,
        в котором  '=' - неживое существо '#'- живое
        """
        space_in_str = ''
        for i in range(1, self.y + 1):
            for j in range(1, self.x + 1):
                space_in_str += str(self.field[i][j])
            space_in_str += '\n'
        return space_in_str

    def is_static(self):
        """
        Метод для сравнения предыдущего и текущего состояния нашей вселенной,
        возвращает True если вселенная статична
        """
        return self.pre_field == self.field

    def clear_pre_verse(self, str_count):
        """Метод для удаления строк в програме, str_count - количество строк для удаления"""
        for i in range(str_count):
            # Символ '\033[F' переводит консольный курсор в начало строки
            # Символ '\033[K' удаляет все символы справа от консольного курсора
            print('\033[F\033[K', end='')


def main():
    """
    Наша основная функция main, тут происходит инициализация нашей вселеной и ее реинкарнация.
    Если вселенная окажется статичной то перерождение прекратится и выведется соответсвующее сообщеие
    """
    print("Если хотите задать своё поле для игры введите 0, иначе 1")
    input_type = input()
    universe = Space(input_type)
    time.sleep(1)
    universe.next_gen()
    while not universe.is_static():
        universe.clear_pre_verse(universe.y + 1)
        print(universe)
        time.sleep(1)
        universe.next_gen()
    universe.clear_pre_verse(universe.y + 1)
    print(universe)
    print("Вселенная статична")


main()
