#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from threading import Lock, Thread
import sympy as sp


"""
Необходимо с использованием многопоточности для заданного значения x найти сумму ряда S 
с точностью члена ряда по абсолютному значению и произвести сравнение полученной суммы с 
контрольным значением функции y(x) для двух бесконечных рядов.
(Вариант 26 (1 и 2)).
"""

E = 1e-7  # Точность
# Создание блокировки для синхронизации доступа к общему ресурсу.
lock = Lock()


def series_1(x, eps, results):
    """
    Функция вычисления суммы ряда задачи №1 (x = 1).
    """
    s = 0
    n = 0
    while True:
        term = x**n * sp.log(3)**n / math.factorial(n)
        if abs(term) < eps:
            break
        s += term
        n += 1
    with lock:
        results["series_1"] = s


def series_2(x, eps, results):
    """
    Функция вычисления суммы ряда задачи №2 (x = 2).
    """
    s = 0
    n = 0
    while True:
        term = x**n
        if abs(term) < eps:
            break
        s += term
        n += 1
    with lock:
        results["series_2"] = s


def main():
    """
    Главная функция программы.
    """
    results = {"series_1": 0, "series_2": 0}

    # Определение символа n
    n = sp.symbols('n')

    # Первое выражение: сумма от n=0 до бесконечности x^n (ln^n 3)/n! при x = 1
    x1 = 1
    control_1 = sp.Sum(x1**n * sp.log(3)**n / sp.factorial(n), (n, 0, sp.oo)).evalf()

    # Второе выражение: сумма от n=0 до бесконечности x^n при x = 0.7
    x2 = 0.7
    control_2 = sp.Sum(x2**n, (n, 0, sp.oo)).evalf()

    thread_1 = Thread(target=series_1, args=(x1, E, results))
    thread_2 = Thread(target=series_2, args=(x2, E, results))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    sum_1 = results["series_1"]
    sum_2 = results["series_2"]

    print(f"x1 = {x1}")
    print(f"Sum of series 1: {sum_1:.7f}")
    print(f"Control value 1: {control_1:.7f}")
    print(f"Match 1: {round(sum_1, 7) == round(control_1, 7)}")

    print(f"x2 = {x2}")
    print(f"Sum of series 2: {sum_2:.7f}")
    print(f"Control value 2: {control_2:.7f}")
    print(f"Match 2: {round(sum_2, 7) == round(control_2, 7)}")


if __name__ == "__main__":
    main()
