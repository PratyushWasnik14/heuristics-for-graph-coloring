import networkx as nx
from matplotlib import pyplot as plt
import time
import os


def parse_dimacs_file(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('e'):
                _, vertex1, vertex2 = line.split()
                vertex1 = int(vertex1)
                vertex2 = int(vertex2)
                if vertex1 not in graph:
                    graph[vertex1] = []
                if vertex2 not in graph:
                    graph[vertex2] = []
                graph[vertex1].append(vertex2)
                graph[vertex2].append(vertex1)
    return graph


def dsatur(graph):
    vertex_colors = {}
    saturation = {vertex: 0 for vertex in graph}
    degrees = {vertex: len(neighbors) for vertex, neighbors in graph.items()}
    current_vertex = max(degrees, key=degrees.get)
    vertex_colors[current_vertex] = 0
    unique_colors = {0}

    while len(vertex_colors) < len(graph):
        uncolored_vertices = [v for v in graph if v not in vertex_colors]
        for vertex in uncolored_vertices:
            adjacent_colors = {vertex_colors.get(neighbor) for neighbor in graph[vertex] if neighbor in vertex_colors}
            saturation[vertex] = len(adjacent_colors)
        current_vertex = max(uncolored_vertices, key=lambda v: (saturation[v], degrees[v]))
        adjacent_colors = {vertex_colors.get(neighbor) for neighbor in graph[current_vertex] if
                           neighbor in vertex_colors}
        color = 0
        while color in adjacent_colors:
            color += 1
        vertex_colors[current_vertex] = color
        unique_colors.add(color)

    return vertex_colors, len(unique_colors)


def visualize_graph(graph, coloring):
    G = nx.Graph()
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(vertex, neighbor)
    color_map = [coloring[node] for node in G.nodes]
    plt.figure(figsize=(12, 12))
    nx.draw(G, with_labels=True, node_color=color_map, cmap=plt.colormaps.get_cmap('tab20'), node_size=500,
            font_size=10, font_color='white', edge_color='gray')
    plt.show()


def write_results_to_file(filename, num_colors, elapsed_time, coloring):
    with open(filename, 'w') as file:
        file.write(f"Number of colors used: {num_colors}\n")
        file.write(f"Elapsed time: {elapsed_time:.2f} seconds\n")
        file.write("Vertex Color Assignments:\n")
        for vertex, color in coloring.items():
            file.write(f"Vertex {vertex}: Color {color}\n")
    os.system(f"notepad.exe {filename}")


file_path = r"C:\Users\Pratyush\Downloads\run test grapgh\flat1000_50_0.dimacs"
result_file = r"C:\Users\Pratyush\Downloads\results.txt"

start_time = time.time()

parsed_graph = parse_dimacs_file(file_path)

dsatur_coloring, num_colors_used = dsatur(parsed_graph)

end_time = time.time()

elapsed_time = end_time - start_time

write_results_to_file(result_file, num_colors_used, elapsed_time, dsatur_coloring)

visualize_graph(parsed_graph, dsatur_coloring)
