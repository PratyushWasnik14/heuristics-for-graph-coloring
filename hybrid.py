import networkx as nx
from matplotlib import pyplot as plt
import concurrent.futures
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


def greedy_coloring(graph):
    # Calculate the degree of each vertex
    vertex_degree = {vertex: len(neighbors) for vertex, neighbors in graph.items()}

    # Sort vertices by degree in descending order
    sorted_vertices = sorted(graph.keys(), key=lambda v: vertex_degree[v], reverse=True)

    vertex_colors = {}
    for vertex in sorted_vertices:
        available_colors = {vertex_colors.get(neighbor) for neighbor in graph[vertex] if neighbor in vertex_colors}
        color = 0
        while color in available_colors:
            color += 1
        vertex_colors[vertex] = color

    return vertex_colors


def independent_sets(graph):
    independent_sets = []
    unprocessed_vertices = set(graph.keys())

    while unprocessed_vertices:
        current_set = set()
        for vertex in list(unprocessed_vertices):
            if all(neighbor not in current_set for neighbor in graph[vertex]):
                current_set.add(vertex)
                unprocessed_vertices.remove(vertex)
        independent_sets.append(current_set)

    return independent_sets


def parallel_dsatur(graph, initial_coloring, num_threads=6, debug_output_file=None):
    independent_sets_list = independent_sets(graph)

    if debug_output_file:
        with open(debug_output_file, 'w') as f:
            f.write("Initial coloring received:\n")
            f.write(str(initial_coloring) + "\n\n")
            num_independent_sets = len(independent_sets_list)
            f.write(f"Total number of independent sets identified: {num_independent_sets}\n\n")
            for i, independent_set in enumerate(independent_sets_list):
                f.write(f"Set {i + 1}: {independent_set}\n")

    # Initialize saturation degrees and seen colors for all vertices
    saturation_degree = {}
    seen_colors = {vertex: set() for vertex in graph}

    for vertex in graph:
        # Update seen colors for neighbors of initially colored vertices
        for neighbor in graph[vertex]:
            if initial_coloring[vertex] not in seen_colors[neighbor]:
                seen_colors[neighbor].add(initial_coloring[vertex])
                saturation_degree[neighbor] = len(seen_colors[neighbor])

    def process_independent_set(vertex_set):
        sub_coloring = initial_coloring.copy()

        if debug_output_file:
            with open(debug_output_file, 'a') as f:
                f.write(f"\nProcessing independent set: {vertex_set}\n")
                f.write(f"Sub-coloring before processing: {sub_coloring}\n")

        for vertex in vertex_set:
            # Find the vertex with the highest saturation degree
            available_colors = {sub_coloring.get(neighbor) for neighbor in graph[vertex] if neighbor in sub_coloring}
            color = 0
            while color in available_colors:
                color += 1
            sub_coloring[vertex] = color

            # Update the saturation degree of neighbors
            for neighbor in graph[vertex]:
                if color not in seen_colors[neighbor]:
                    seen_colors[neighbor].add(color)
                    saturation_degree[neighbor] = len(seen_colors[neighbor])

        if debug_output_file:
            with open(debug_output_file, 'a') as f:
                f.write(f"Sub-coloring after processing: {sub_coloring}\n")
        return sub_coloring

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_independent_set, vertex_set) for vertex_set in independent_sets_list]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    # Consolidate all results and resolve conflicts
    final_coloring = initial_coloring.copy()
    if debug_output_file:
        with open(debug_output_file, 'a') as f:
            f.write("\n Merging results from independent sets...\n")
    for result in results:
        for vertex, color in result.items():
            if vertex in final_coloring and final_coloring[vertex] != color:
                if debug_output_file:
                    with open(debug_output_file, 'a') as f:
                        f.write(
                            f"Conflict detected at vertex {vertex}: Existing color {final_coloring[vertex]}, New color {color}\n")
                final_coloring[vertex] = min(final_coloring[vertex], color)
                if debug_output_file:
                    with open(debug_output_file, 'a') as f:
                        f.write(f"Resolved conflict at vertex {vertex}: Chose color {final_coloring[vertex]}\n")
            else:
                final_coloring[vertex] = color

    # Post-process to ensure there are no conflicts left and update saturation degrees
    for vertex in graph:
        available_colors = {final_coloring.get(neighbor) for neighbor in graph[vertex] if neighbor in final_coloring}
        if final_coloring[vertex] in available_colors:
            # Conflict detected, resolve by choosing the lowest available color
            color = 0
            while color in available_colors:
                color += 1
            final_coloring[vertex] = color

            # Update the saturation degree of neighbors after resolving conflict
            for neighbor in graph[vertex]:
                if color not in seen_colors[neighbor]:
                    seen_colors[neighbor].add(color)
                    saturation_degree[neighbor] = len(seen_colors[neighbor])

    num_colors_used = len(set(final_coloring.values()))

    if debug_output_file:
        with open(debug_output_file, 'a') as f:
            f.write(f"\nFinal number of colors used: {num_colors_used}\n")

    return final_coloring, num_colors_used


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


def write_results_to_file(filename, num_colors, elapsed_time, refined_coloring):
    with open(filename, 'w') as file:
        file.write(f"Number of colors used: {num_colors}\n")
        file.write(f"Elapsed time: {elapsed_time:.2f} seconds\n")
        file.write("Vertex Color Assignments:\n")
        for vertex, color in refined_coloring.items():
            file.write(f"Vertex {vertex}: Color {color}\n")
    os.system(f"notepad.exe {filename}")


file_path = r"C:\Users\Pratyush\Downloads\run test grapgh\graph_1000v_1000e.dimacs"
result_file = r"C:\Users\Pratyush\Downloads\results.txt"
debug_output_file = r"C:\Users\Pratyush\Downloads\debug_output.txt"  # Add a file for detailed output

start_time = time.time()

# Step 1: Parse the graph from the file
graph = parse_dimacs_file(file_path)

# Step 2: Get the initial coloring using the greedy heuristic
initial_coloring = greedy_coloring(graph)

# Step 3: Run the parallel DSATUR algorithm with the initial coloring and detailed debug output
refined_coloring, num_colors = parallel_dsatur(graph, initial_coloring, debug_output_file=debug_output_file)

end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Write the results to the file
write_results_to_file(result_file, num_colors, elapsed_time, refined_coloring)

# Optionally visualize the graph with the refined coloring
visualize_graph(graph, refined_coloring)
