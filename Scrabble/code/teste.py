# Lista de tuplas
lista = [(3, 8), (1, 5), (2, 7), (4, 6)]

# Direção (h para horizontal, v para vertical)
direcao = 'h'

# Ordenar a lista usando uma função lambda como chave de ordenação
lista_ordenada = sorted(lista, key=lambda tupla: tupla[0] if direcao == "h" else tupla[1])

# Imprimir lista ordenada
print(lista_ordenada)