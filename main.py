import flet as ft
import heapq
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image

# algoritmo de dijkstra
def dijkstra(grafo, inicio):
    fila = [(0, inicio)]
    dist = {no: float('inf') for no in grafo}
    dist[inicio] = 0
    caminho = {no: [] for no in grafo}
    caminho[inicio] = [inicio]

    while fila:
        distancia_atual, no_atual = heapq.heappop(fila)

        if distancia_atual > dist[no_atual]:
            continue

        for vizinho, peso in grafo[no_atual]:
            nova_distancia = distancia_atual + peso

            if nova_distancia < dist[vizinho]:
                dist[vizinho] = nova_distancia
                heapq.heappush(fila, (nova_distancia, vizinho))
                caminho[vizinho] = caminho[no_atual] + [vizinho]

    return dist, caminho

# desenho do grafo
def desenhar_grafo(grafo, caminho, start_node):
    G = nx.Graph()
    for no, vizinhos in grafo.items():
        for vizinho, peso in vizinhos:
            G.add_edge(no, vizinho, weight=peso)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))

    # desenho dos nós e arestas
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2500, edge_color='k', font_size=16, font_weight='bold')

    # desenho do caminho mais curto
    if start_node in caminho:
        path_edges = list(zip(caminho[start_node], caminho[start_node][1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

    plt.title(f'Caminho Mais Curto a partir do Nó {start_node}')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

# interface grafica
def main(page: ft.Page):
    page.title = "Algoritmo de Dijkstra"
    page.window_width = 800
    page.window_height = 600

    grafo = {}

    def adicionar_aresta(e):
        no1 = no1_input.value
        no2 = no2_input.value
        peso = int(peso_input.value)

        if no1 not in grafo:
            grafo[no1] = []
        if no2 not in grafo:
            grafo[no2] = []

        grafo[no1].append((no2, peso))
        grafo[no2].append((no1, peso))

        arestas_view.controls.append(ft.Text(f"{no1} --({peso})--> {no2}"))
        no1_input.value = ""
        no2_input.value = ""
        peso_input.value = ""
        page.update()

    def calcular_distancias(e):
        no_inicial = no_inicial_input.value
        if no_inicial not in grafo:
            resultado_view.controls.clear()
            resultado_view.controls.append(ft.Text(f"Nó inicial {no_inicial} não existe no grafo."))
            page.update()
            return

        distancias, caminho = dijkstra(grafo, no_inicial)
        resultado_view.controls.clear()
        resultado_view.controls.append(ft.Text(f"Distâncias mínimas a partir do nó {no_inicial}:"))
        for no, distancia in distancias.items():
            resultado_view.controls.append(ft.Text(f"{no_inicial} -> {no}: {distancia}"))

        buf = desenhar_grafo(grafo, caminho, no_inicial)
        img_data = buf.getvalue()
        img_src = base64.b64encode(img_data).decode()
        img_element = ft.Image(src_base64=img_src, width=600, height=450)
        
        resultado_view.controls.append(
            ft.Row([img_element], alignment=ft.MainAxisAlignment.CENTER)
        )

        page.update()

    no1_input = ft.TextField(label="Nó 1")
    no2_input = ft.TextField(label="Nó 2")
    peso_input = ft.TextField(label="Peso", keyboard_type=ft.KeyboardType.NUMBER)
    no_inicial_input = ft.TextField(label="Nó Inicial")

    adicionar_aresta_button = ft.ElevatedButton(text="Adicionar Aresta", on_click=adicionar_aresta)
    calcular_button = ft.ElevatedButton(text="Calcular Distâncias", on_click=calcular_distancias)

    arestas_view = ft.Column()
    resultado_view = ft.Column()

    page.add(
        ft.Column([
            ft.Row([no1_input, no2_input, peso_input, adicionar_aresta_button]),
            ft.Row([no_inicial_input, calcular_button]),
            arestas_view,
            resultado_view
        ])
    )

# exec da interface
ft.app(target=main)
