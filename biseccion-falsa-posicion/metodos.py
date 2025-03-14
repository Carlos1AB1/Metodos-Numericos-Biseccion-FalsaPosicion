import numpy as np


def biseccion(func, a, b, tol, max_iter):
    iteraciones = []
    if func(a) * func(b) >= 0:
        return None  # No hay cambio de signo en el intervalo

    xr = (a + b) / 2
    for i in range(max_iter):
        xr_ant = xr
        xr = (a + b) / 2
        fxr = func(xr)
        Ea = abs((xr - xr_ant) / xr) * 100 if i > 0 else None

        iteraciones.append([i + 1, a, xr, b, fxr, Ea])

        if fxr == 0 or (Ea is not None and Ea < tol):
            break

        if func(a) * fxr < 0:
            b = xr
        else:
            a = xr

    return iteraciones


def falsa_posicion(func, a, b, tol, max_iter):
    iteraciones = []  # Inicializamos la lista aquí

    print(f"f({a}) = {func(a)}, f({b}) = {func(b)}")  # Depuración

    if func(a) * func(b) >= 0:
        return None  # No hay cambio de signo en el intervalo

    xr = a  # Definimos xr inicial para la primera iteración
    for i in range(max_iter):
        xr_ant = xr
        xr = (a * func(b) - b * func(a)) / (func(b) - func(a))
        fxr = func(xr)
        Ea = abs((xr - xr_ant) / xr) * 100 if i > 0 else None  # Evitamos la primera división

        iteraciones.append([i + 1, a, xr, b, fxr, Ea])

        if fxr == 0 or (Ea is not None and Ea < tol):
            break

        if func(a) * fxr < 0:
            b = xr
        else:
            a = xr

    return iteraciones  # Aseguramos que devuelve la lista
