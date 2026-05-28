"""
Atividade 1 Árvore de Espalhamento Mínimo
Algoritmos: Kruskal e PRIM
"""

import heapq
import os

# leitura do arquivo de instância
# ============================================================

def ler_instancia(caminho):
    """
    Lê o arquivo de instância e retorna:
      - n: número de vértices
      - matriz: matriz de adjacência completa e simétrica
    """
    with open(caminho, 'r') as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]

    n = int(linhas[0])
    matriz = [[0] * n for _ in range(n)]

    for i in range(n - 1):
        valores = list(map(int, linhas[i + 1].split())) # split para separar os valores da linha
        for k, j in enumerate(range(i + 1, n)): # monta matriz
            matriz[i][j] = valores[k]
            matriz[j][i] = valores[k]  

    return n, matriz


# estrutura auxiliar para o Kruskal
# ============================================================

class UnionFind:
    """
    Union-Find com:
      - compressão de caminho no 'encontrar'
      - união por rank para manter a árvore balanceada
    
    Serve para verificar rapidamente se dois vértices
    já fazem parte do mesmo componente conectado.
    """

    def __init__(self, n):
        self.pai = list(range(n))   # cada vértice é pai de si mesmo
        self.rank = [0] * n

    def encontrar(self, x):
        """Retorna a raiz do conjunto de x"""
        if self.pai[x] != x:
            self.pai[x] = self.encontrar(self.pai[x])  # compressão de caminho
        return self.pai[x]

    def unir(self, x, y):
        """
        Une os conjuntos de x e y.
        Retorna True se a união foi feita (não estavam no mesmo conjunto).
        Retorna False se já estavam no mesmo conjunto (formaria ciclo).
        """
        raiz_x = self.encontrar(x)
        raiz_y = self.encontrar(y)

        if raiz_x == raiz_y:
            return False  # mesma componente — adicionaria ciclo

        # Une pelo rank para manter a árvore mais achatada
        if self.rank[raiz_x] < self.rank[raiz_y]:
            raiz_x, raiz_y = raiz_y, raiz_x

        self.pai[raiz_y] = raiz_x
        if self.rank[raiz_x] == self.rank[raiz_y]:
            self.rank[raiz_x] += 1

        return True


# ============================================================
# Algoritmo de Kruskal
# ============================================================

def construir_lista_arestas(n, matriz):
    """
    Extrai todas as arestas do triângulo superior da matriz.
    Retorna lista de tuplas (peso, u, v).
    """
    arestas = []
    for i in range(n):
        for j in range(i + 1, n):
            arestas.append((matriz[i][j], i, j))
    return arestas


def kruskal(n, matriz):
    """
    Algoritmo de Kruskal — Árvore de Espalhamento Mínimo.

    Ideia gulosa:
      1. Ordena todas as arestas do menor para o maior peso.
      2. Percorre as arestas em ordem crescente de peso.
      3. Adiciona a aresta na árvore se ela NÃO formar ciclo.
      4. Para quando a árvore tiver n-1 arestas.

    Retorna o custo total da árvore mínima.
    """
    arestas = construir_lista_arestas(n, matriz)
    arestas.sort()  # ordena pelo peso 

    uf = UnionFind(n)
    custo_total = 0
    arestas_adicionadas = 0

    for peso, u, v in arestas:
        if uf.unir(u, v):           # adiciona apenas se nao forma ciclo
            custo_total += peso
            arestas_adicionadas += 1
            if arestas_adicionadas == n - 1:
                break               # árvore completa com n-1 arestas

    return custo_total


# Algoritmo de PRIM

def prim(n, matriz):
    """
    Algoritmo de PRIM — Árvore de Espalhamento Mínimo.

    Ideia gulosa:
      1. Começa com o vértice 0 na árvore.
      2. A cada passo, escolhe a aresta de menor peso que
         conecta um vértice já na árvore a um vértice fora dela.
      3. Adiciona esse vértice à árvore e repete até todos estarem incluídos.

    Usa uma fila de prioridade (min-heap) para selecionar
    eficientemente a menor aresta disponível.

    Retorna o custo total da árvore mínima.
    """
    visitado = [False] * n
    menor_custo = [float('inf')] * n
    menor_custo[0] = 0              # vértice 0 é o ponto de partida

    heap = [(0, 0)]                 # (custo para entrar na árvore, vértice)
    custo_total = 0

    while heap:
        custo, u = heapq.heappop(heap)

        if visitado[u]:
            continue                # entrada desatualizada na heap — descarta

        visitado[u] = True
        custo_total += custo

        # Verifica todos os vizinhos de u ainda fora da árvore
        for v in range(n):
            if not visitado[v] and matriz[u][v] < menor_custo[v]:
                menor_custo[v] = matriz[u][v]
                heapq.heappush(heap, (menor_custo[v], v))

    return custo_total

# ============================================================

def main():
    pasta_instancias = 'instancias_Dijkstra_PRIM_Kruskal'
    instancias = ['dij10.txt', 'dij20.txt', 'dij40.txt', 'dij50.txt']

    print()
    print("=" * 58)
    print("  Atividade 1 - Árvore de Espalhamento Mínimo")
    print("=" * 58)
    print(f"  {'Instância':<12} {'Kruskal':>14} {'PRIM':>14}")
    print("  " + "-" * 44)

    for nome_arquivo in instancias:
        caminho = os.path.join(pasta_instancias, nome_arquivo)

        n, matriz = ler_instancia(caminho)

        custo_kruskal = kruskal(n, matriz)
        custo_prim = prim(n, matriz)

        instancia = nome_arquivo.replace('.txt', '')
        print(f"  {instancia:<12} {custo_kruskal:>14} {custo_prim:>14}")

    print("=" * 58)
    print()


if __name__ == '__main__':
    main()
