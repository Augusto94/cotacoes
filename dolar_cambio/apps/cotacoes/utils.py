def chunks(lista, n):
    for i in range(0, len(lista), n):
        yield lista[i : i + n]
