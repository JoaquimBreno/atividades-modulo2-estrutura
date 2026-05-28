"""
Atividade 3 - Problema da Mochila Inteira
Algoritmo: Programação Dinâmica

pra instancias grandes só mostra o valor
porque montar a tabela 2D inteira estoura a memória
"""

import os


# leitura do arquivo
# ============================================================

def ler_instancia(caminho):
    """
    Le o arquivo e retorna:
      - n: quantidade de itens
      - M: capacidade da mochila
      - pesos:  lista com o peso de cada item
      - valores: lista com o valor de cada item
    """
    with open(caminho, 'r') as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]

    n, M = map(int, linhas[0].split())  # primeira linha: n e M

    pesos  = []
    valores = []
    for linha in linhas[1:n + 1]:
        p, v = map(int, linha.split())
        pesos.append(p)
        valores.append(v)

    return n, M, pesos, valores


# ============================================================
# DP com tabela 2D - usado quando a instancia é pequena
# permite saber quais itens foram escolhidos

def mochila_com_itens(n, M, pesos, valores):
    """
    Programação Dinâmica com tabela completa.

    Ideia:
      - dp[i][w] = melhor valor usando os i primeiros itens com capacidade w
      - pra cada item escolhe: coloca ou nao coloca
      - se colocar, subtrai o peso e soma o valor
      - ao final, volta na tabela pra descobrir quais itens entraram

    Retorna o valor ótimo e a lista de itens escolhidos (índice começa em 1).
    """
    # monta a tabela zerada
    dp = [[0] * (M + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(M + 1):
            dp[i][w] = dp[i - 1][w]  # nao coloca o item i
            if pesos[i - 1] <= w:    # cabe na mochila?
                com_item = dp[i - 1][w - pesos[i - 1]] + valores[i - 1]
                if com_item > dp[i][w]:
                    dp[i][w] = com_item  # coloca o item i

    # volta na tabela pra ver quais itens entrarm
    itens = []
    w = M
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:   # esse item foi escolhido
            itens.append(i)
            w -= pesos[i - 1]

    return dp[n][M], sorted(itens)


# ============================================================
# DP com array 1D  usado quando a instancia é grande

def mochila_so_valor(n, M, pesos, valores):
    """
    Programação Dinâmica com array 1D (rolante).

    Ideia:
      - dp[w] = melhor valor com capacidade w
      - percorre os itens um a um, atualizando dp de trás pra frente
        (de trás pra frente evita usar o mesmo item mais de uma vez)

    Retorna só o valor ótimo.
    """
    dp = [0] * (M + 1)

    for i in range(n):
        # percorre de trás pra frente pra nao reusar o item
        for w in range(M, pesos[i] - 1, -1):
            com_item = dp[w - pesos[i]] + valores[i]
            if com_item > dp[w]:
                dp[w] = com_item

    return dp[M]


# ============================================================

# limite pra decidir qual versão usar
# acima disso a tabela 2D seria grande demais
LIMITE_2D = 15_000_000   # ~100MB de memoria


def main():
    pasta = 'instancias_Mochila'
    instancias = [
        'mochila01.txt',
        'mochila02.txt',
        'mochila1000.txt',
        'mochila2500.txt',
        'mochila5000.txt',
    ]

    print()
    print("=" * 58)
    print("  Atividade 3 - Problema da Mochila Inteira (DP)")
    print("=" * 58)

    for nome_arquivo in instancias:
        caminho = os.path.join(pasta, nome_arquivo)
        n, M, pesos, valores = ler_instancia(caminho)

        instancia = nome_arquivo.replace('.txt', '')
        print(f"\n  instância : {instancia}")
        print(f"  itens     : {n}   capacidade: {M}")

        if n * M <= LIMITE_2D:
            # instancia pequena — monta tabela completa e lista os itens
            valor, itens = mochila_com_itens(n, M, pesos, valores)
            print(f"  valor     : {valor}")
            print(f"  itens escolhidos: {', '.join(map(str, itens))}")
        else:
            # instancia grande — só calcula o valor
            valor = mochila_so_valor(n, M, pesos, valores)
            print(f"  valor     : {valor}")
            print(f"  itens escolhidos: (instancia grande, nao listado)")

    print()
    print("=" * 58)
    print()


if __name__ == '__main__':
    main()
