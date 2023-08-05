import math
import matplotlib.pyplot as plt
import numpy

class DemoException(Exception):
    """
    Classe para criar exceções personalizadas
    """
    def __init__(self, message):
        super().__init__(message)

message = "ValueError: fatorial() not defined for negative values."
message0 = "ValueError: raiz() not defined for negative values."
message1 = "TypeError: 'float' object cannot be interpreted as an integer."
message2 = "OverflowError: mat range error."

def emcima(numero):
    """
    modulo para arredodar um numero para cima

    parametros: numero

    :return: Retorna o valor arredondado para cima
    """
    part = numero % 1
    if part == 0:
        if numero > 0:
            numero = int(numero)
            return numero
        else:
            numero = int(numero)
            return numero
    else:
        if numero > 0:
            numero = int(numero)
            return numero + 1
        else:
            numero = int(numero)
            return numero

def embaixo(numero):
    """
        modulo para arredodar um numero para baixo

        parametros: numero

        :return: Retorna o valor arredondado para baixo
        """
    part = numero % 1
    if part == 0:
        if numero > 0:
            numero = int(numero)
            return numero
        else:
            numero = int(numero)
            return numero
    else:
        if numero > 0:
            numero = int(numero)
            return numero
        else:
            numero = int(numero)
            return numero - 1

def raiz(numero):
    """
        modulo para calcular a raiz quadrada de um numero inteiro não negativo

        parametros: numero

        :return: Retorna a raiz do numero dado
        """
    j = 1
    cont = 0
    part = numero % 1
    if part == 0:
        if numero < 0:
            raise DemoException(message0)
        else:
            while numero != 0:
                numero = numero - j
                if numero < 0:
                    break
                else:
                    j = j + 2
                    cont = cont + 1
    else:
        raise DemoException(message1)
    return cont

def binario(numero):
    """
        modulo para transformar um numero não negativo em binario

        parametros: numero

        :return: Retorna o valor dado em binario
        """
    if numero > 0:
        part = numero % 1
        if part == 0:
            b = list()
            bina = ''
            j = 0
            while numero != 0:
                i = numero % 2
                i = str(i)
                b.append(i)
                j += 1
                numero = numero // 2
            j = j - 1
            while j >= 0:
                bina = bina + b[j]
                j -= 1
            return bina
        else:
            numero = int(numero)
            b = list()
            bina = ''
            j = 0
            while numero != 0:
                i = numero % 2
                i = str(i)
                b.append(i)
                j += 1
                numero = numero // 2
            j = j - 1
            while j >= 0:
                bina = bina + b[j]
                j -= 1
            return bina
    else:
        raise DemoException(message0)

def fatorial(numero):
    """
        modulo para calcular o fatorial de numeros inteiros maiores que 0 e menores que 100

        parametros: numero

        :return: Retorna o fatorial do numero dado
    """

    part = numero % 1
    fat = 1
    if part == 0:
        if numero > 100:
            raise DemoException(message2)
        elif numero <= 0:
            raise DemoException(message)
        else:
            while numero != 1:
                fat = fat * numero
                numero = numero - 1
    else:
        raise DemoException(message1)
    return fat

def potencia(base, exp):
    """
        modulo para calcular a exponenciação

        parametros: base, exp

        :return: Retorna o valor da base elevado a exp
    """

    cont = 0
    pot = 1
    part = exp % 1
    if part == 0:
        if exp < 0:
            exp = exp * - 1
            base = 1 / base
            while cont != exp:
                pot = pot * base
                cont += 1
        else:
            while cont != exp:
                pot = pot * base
                cont += 1
    else:
        raise DemoException(message1)
    return pot

def seno(numero):
    """
        modulo para calcular o seno de um ângulo

        parametros: numero

        :return: Retorna o valor do seno do ângulo do numero dado
    """

    x = numpy.linspace(0, 2 * numpy.pi, 100)
    y = numpy.sin(x)
    plt.plot(x, y)
    plt.title('SENO')
    plt.show()
    seno = math.sin(math.radians(numero))
    return seno

def cosseno(numero):
    """
        modulo para calcular o cosseno de um ângulo

        parametros: numero

        :return: Retorna o valor do cosseno do ângulo do numero dado
    """

    x = numpy.linspace(0, 2 * numpy.pi, 100)
    y = numpy.cos(x)
    plt.plot(x, y)
    plt.title('COSSENO')
    plt.show()
    cosseno = math.cos(math.radians(numero))
    return cosseno

def tangente(numero):
    """
        modulo para calcular a tangente de um ângulo

        parametros: numero

        :return: Retorna o valor da tangente do ângulo do numero dado
    """

    x = numpy.linspace(0, 2 * numpy.pi, 100)
    y = numpy.tan(x)
    plt.plot(x, y)
    plt.title('Tangente')
    plt.show()
    tangente = math.tan(math.radians(numero))
    return tangente

def equa(A, B, C):
    """
        modulo para calcular uma equação quadrática completa

        parametros: A, B, C

        :return: Retorna o valor das raizes da equação
    """

    if B == 0 or C == 0:
        return False
    else:
        delta = B*B-4*A*C
        if delta < 0:
            return False
        else:
            x1 = (-B+(math.sqrt(delta))) / 2*A
            x2 = (-B-(math.sqrt(delta))) / 2*A
            x = numpy.linspace(-numpy.pi,  numpy.pi, 100)
            y = A*x**2 + B*x + C
            plt.plot(x, y)
            plt.title('Equação Quadrática')
            plt.show()
            return x1, x2

def loga(numero, base):
    """
        modulo para calcular uma função logaritmica de um numero natural

        parametros: numero, base

        :return: Retorna o valor do log de um numero dado
    """

    x = numpy.linspace(numero, base, 100)
    y = numpy.log(x)
    plt.plot(x, y)
    plt.title('LOG')
    plt.show()
    loga = math.log(numero, base)
    return loga