import random

import networkx as nx
import matplotlib.pyplot as plt

"""
pragma threads=1;
CREATE TABLE R AS FROM read_csv('/Users/paul/workspace/generic_data_benchmark/src/playground/networkx_graphs/data/powerlaw_cluster.csv');
EXPLAIN ANALYZE SELECT R1.a AS A, R2.a AS B, R3.a AS C FROM R R1 JOIN R R2 ON R1.b = R2.a JOIN R R3 ON R2.b = R3.a WHERE R3.b = R1.a;
"""
def generate_graph(graph_type, **kwargs):
    if graph_type == 'erdos_renyi':
        return nx.erdos_renyi_graph(kwargs['n'], kwargs['p'])
    elif graph_type == 'barabasi_albert':
        return nx.barabasi_albert_graph(kwargs['n'], kwargs['m'])
    elif graph_type == 'watts_strogatz':
        return nx.watts_strogatz_graph(kwargs['n'], kwargs['k'], kwargs['p'])
    elif graph_type == 'regular_lattice':
        return nx.grid_2d_graph(kwargs['m'], kwargs['n'])
    elif graph_type == 'powerlaw_cluster':
        return nx.powerlaw_cluster_graph(kwargs['n'], kwargs['m'], kwargs['p'])
    else:
        raise ValueError("Unsupported graph type")


def plot_graph_and_distribution(G, title="Graph", plot_graph=True):
    edge_distribution_in = [d for u, d in G.in_degree()]
    edge_distribution_out = [d for u, d in G.out_degree()]

    fig, ax = plt.subplots(1, 3, figsize=(18, 6))

    if plot_graph:
        # Plot graph
        plt.sca(ax[0])
        nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=100, font_size=0, arrowsize=10)
        plt.title(title)

    # Plot in-degree distribution
    plt.sca(ax[1])
    plt.hist(edge_distribution_in, bins=20, color='lightblue', edgecolor='gray')
    plt.yscale('log')
    plt.title("In-Degree Distribution")

    # Plot out-degree distribution
    plt.sca(ax[2])
    plt.hist(edge_distribution_out, bins=20, color='lightblue', edgecolor='gray')
    plt.yscale('log')
    plt.title("Out-Degree Distribution")

    plt.tight_layout()

    # save the plot as a png file
    plt.savefig(f'networkx_graphs/plots/{title}.png')

    plt.show()


def save_edge_table_as_csv(G, filename):
    with open(filename, 'w') as f:
        f.write('a,b\n')
        for u, v in G.edges():
            f.write(f'{u},{v}\n')


def make_directed(G, forward_prob=0.5):
    # Create a new directed graph
    DG = nx.DiGraph()

    # For each edge in the undirected graph, randomly assign a direction based on the given probability
    for u, v in G.edges():
        if random.random() < forward_prob:
            DG.add_edge(u, v)
        else:
            DG.add_edge(v, u)

    return DG


# Example usage
if __name__ == "__main__":

    nodes = 100_000
    edges_per_node = 16

    # Parameters for different graph types
    params = {
        # 'erdos_renyi': {'n': nodes, 'p': 0.1},
        # 'barabasi_albert': {'n': nodes, 'm': 2},
        # 'watts_strogatz': {'n': 256, 'k': 4, 'p': 0.1},
        # 'regular_lattice': {'m': 15, 'n': 15},
        'powerlaw_cluster': {'n': nodes, 'm': edges_per_node, 'p': 0.1},
    }

    # Generate and draw graphs
    for graph_type in params:
        G = generate_graph(graph_type, **params[graph_type])
        # make graph directed
        G = make_directed(G)

        plot_graph_and_distribution(G, title=graph_type, plot_graph=nodes <= 512)

        # save edge table as csv
        save_edge_table_as_csv(G, f'networkx_graphs/data/{graph_type}.csv')
