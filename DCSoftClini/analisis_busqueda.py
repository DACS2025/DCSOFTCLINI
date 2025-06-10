

def generar_serie_aritmetica(inicio, diferencia, cantidad):
    return [inicio + i * diferencia for i in range(cantidad)]

def busqueda_lineal(lista, objetivo):
    inicio, fin = 0, len(lista) - 1
    contador = 0
    posicion = inicio
    while posicion <= fin:
        valor = lista[posicion]
        contador = contador + 1
        if valor == objetivo:
            return f"Búsqueda lineal: Encontrado en la posición {posicion+1} contador de busquedas {contador}"
        posicion += 1

    return f"No encontrado, número de búsquedas: {contador}"


def busqueda_binaria(lista, objetivo):
    inicio, fin = 0, len(lista) - 1
    contador = 0
    while inicio <= fin:
        medio = (inicio + fin) // 2
        valor_medio = lista[medio]
        contador = contador + 1
        if valor_medio == objetivo:
            return f"Busqueda binaria: Encontrado en la posición {medio+1} contador de busquedas {contador}"
        elif valor_medio < objetivo:
            inicio = medio + 1
        else:
            fin = medio - 1

    return f"No encontrado, número de búsquedas: {contador}"

# Generamos la serie aritmética
lista = generar_serie_aritmetica(inicio=3, diferencia=5, cantidad=1000000)

# Mostrar la lista generada
print("Número de elementos de la lista generada:", len(lista))

# Solicitar número al usuario
try:
    numero_buscado = int(input("Ingrese el número a buscar: "))
    resultado = busqueda_binaria(lista, numero_buscado)
    print(resultado)

    resultado = busqueda_lineal(lista, numero_buscado)
    print(resultado)

except ValueError:
    print("Por favor, ingrese un número válido.")
