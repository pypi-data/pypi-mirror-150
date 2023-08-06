# В основе метода библиотеки dis - анализ кода с помощью его дизассемблирования
# (разбор кода на составляющие: в нашем случае - на атрибуты и методы класса)
# https://docs.python.org/3/library/dis.html

import dis


# Metaclass для проверки соответствия сервера
# Метакласс для проверки соответствия сервера:
class ServerMaker(type):
    def __init__(cls, clsname, bases, clsdict):
        # Список методов, которые используются в функциях класса:
        methods = []
        # Атрибуты, вызываемые функциями классов
        attrs = []
        for func in clsdict:
            # Пробуем
            try:
                ret = dis.get_instructions(clsdict[func])
                # Если не функция то ловим исключение
            except TypeError:
                pass
            else:
                # Раз функция разбираем код, получая используемые методы и атрибуты.
                for i in ret:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
        # Если обнаружено использование недопустимого метода connect, бросаем исключение:
        if 'connect' in methods:
            raise TypeError('Использование метода connect недопустимо в серверном классе')
        # Если сокет не инициализировался константами SOCK_STREAM(TCP) AF_INET(IPv4), тоже исключение.
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета.')
        super().__init__(clsname, bases, clsdict)


# Metaclass для проверки корректности клиентов

class ClientMaker(type):
    def __init__(cls, clsname, bases, clsdict):
        methods = []
        for func in clsdict:
            try:
                # Возвращаем итератор по инструкции в представленной функции,
                # методе, строке исходного кода или объекте кода
                ret = dis.get_instructions(clsdict[func])
                # Если не функция то ловим исключение
                # (если порт)
            except TypeError:
                pass
            else:
                # Раз функция разбираем код получая используемы методы и атрибуты
                for i in ret:

                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            # Заполняем список методами, использующимися в функциях класса
                            methods.append(i.argval)

        # Если обнаружено использование недопустимого метода accept,
        # listen, socket бросаем исключение
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError('В классе используется запрещенный метод')
        if 'get_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами')
        super().__init__(clsname, bases, clsdict)
