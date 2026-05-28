"""
Atividade 2 - Caminho Mínimo
Algoritmo: Dijkstra

Para todas as instâncias: origem = 0, destino = n - 1
"""

import heapq
import os


# leitura do arquivo de instância
# ============================================================

def ler_instancia(caminho):
    
    with open(caminho, 'r') as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]

    n = int(linhas[0])
    adjacencia = [[] for _ in range(n)]

    for i in range(n - 1):
        valores = list(map(int, linhas[i + 1].split()))  # split para separar os valores da linha
        for k, j in enumerate(range(i + 1, n)):          # monta lista de adjacência
            dist = valores[k]
            adjacencia[i].append((j, dist))   # aresta i → j
            adjacencia[j].append((i, dist))   # aresta j → i 

    return n, adjacencia


# ============================================================
# Algoritmo de Dijkstra

def dijkstra(n, adjacencia, origem, destino):
    """
    Algoritmo de Dijkstra — Caminho Mínimo de origem até destino.

    Ideia gulosa:
      1. Começa com distância 0 na origem e infinito nos demais vértices.
      2. A cada passo, escolhe o vértice não visitado com menor distância
         acumulada (usando uma fila de prioridade / min-heap).
      3. Tenta melhorar a distância de cada vizinho (relaxamento da aresta).

    Retorna a menor distância da origem ao destino.
    """
    distancia = [float('inf')] * n
    distancia[origem] = 0

    visitado = [False] * n
    heap = [(0, origem)]        # (distância acumulada, vértice)

    while heap:
        dist_atual, u = heapq.heappop(heap)

        if visitado[u]:
            continue            # entrada desatualizada na heap — descarta

        visitado[u] = True

        if u == destino:
            break               # chegamos ao destino — podemos parar

        # tenta encurtar o caminho para cada vizinho de u
        for v, peso in adjacencia[u]:
            nova_dist = dist_atual + peso
            if nova_dist < distancia[v]:
                distancia[v] = nova_dist
                heapq.heappush(heap, (nova_dist, v))

    return distancia[destino]


# ============================================================

def main():
    pasta_instancias = 'instancias_Dijkstra_PRIM_Kruskal'
    instancias = ['dij10.txt', 'dij20.txt', 'dij40.txt', 'dij50.txt']

    print()
    print("=" * 58)
    print("  Atividade 2 - Caminho Mínimo (Dijkstra)")
    print("=" * 58)
    print(f"  {'Instância':<12} {'Origem':>8} {'Destino':>9} {'Distância':>14}")
    print("  " + "-" * 44)

    for nome_arquivo in instancias:
        caminho = os.path.join(pasta_instancias, nome_arquivo)

        n, adjacencia = ler_instancia(caminho)

        origem  = 0
        destino = n - 1

        distancia_minima = dijkstra(n, adjacencia, origem, destino)

        instancia = nome_arquivo.replace('.txt', '')
        print(f"  {instancia:<12} {origem:>8} {destino:>9} {distancia_minima:>14}")

    print("=" * 58)
    print()


if __name__ == '__main__':
    main()
