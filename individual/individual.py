#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from threading import Lock, Thread
import sympy as sp


"""
Необходимо с использованием многопоточности для заданного значения x найти сумму ряда S 
с точностью члена ряда по абсолютному значению и произвести сравнение полученной суммы с 
контрольным значением функции y(x) для двух бесконечных рядов (Вариант 26 (1 и 2)).
"""

E = 1e-7  # Точность
# Создание блокировки для синхронизации доступа к общему ресурсу.
lock = Lock()


def series1(x, eps, results):
    s = 0
    n = 0
    while True:
        term = x**n * sp.log(3)**n / math.factorial(n)
        if abs(term) < eps:
            break
        s += term
        n += 1
    with lock:
        results["series1"] = s


def series2(x, eps, results):
    s = 0
    n = 0
    while True:
        term = x**n
        if abs(term) < eps:
            break
        s += term
        n += 1
    with lock:
        results["series2"] = s


def main():
    results = {"series1": 0, "series2": 0}

    # Определение символа n
    n = sp.symbols('n')

    # Первое выражение: сумма от n=0 до бесконечности x^n (ln^n 3)/n! ; x=1
    x1 = 1
    control1 = sp.Sum(x1**n * sp.log(3)**n / sp.factorial(n), (n, 0, sp.oo)).evalf()

    # Второе выражение: сумма от n=0 до бесконечности x^n ; x=0.7
    x2 = 0.7
    control2 = sp.Sum(x2**n, (n, 0, sp.oo)).evalf()

    thread1 = Thread(target=series1, args=(x1, E, results))
    thread2 = Thread(target=series2, args=(x2, E, results))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    sum1 = results["series1"]
    sum2 = results["series2"]

    print(f"x1 = {x1}")
    print(f"Sum of series 1: {sum1:.7f}")
    print(f"Control value 1: {control1:.7f}")
    print(f"Match 1: {round(sum1, 7) == round(control1, 7)}")

    print(f"x2 = {x2}")
    print(f"Sum of series 2: {sum2:.7f}")
    print(f"Control value 2: {control2:.7f}")
    print(f"Match 2: {round(sum2, 7) == round(control2, 7)}")


if __name__ == "__main__":
    main()
