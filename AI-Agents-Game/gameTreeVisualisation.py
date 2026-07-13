import matplotlib.pyplot as plt
import networkx as nx

def create_game_tree(move_storage):
    G = nx.DiGraph()

    G.add_node("Start", label="Start\n(empty board)")
    parent = "Start"
    
    for i, (player, col) in enumerate(move_storage):
        node_id = f"{player}_{i}"  #move id 
        move_label = f"{player} moved to column {col}"
        combined_label = f"{node_id}\n{move_label}"  #so we can see the player and the move in the node label under the node id
        G.add_node(node_id, label=combined_label)
        G.add_edge(parent, node_id)
        parent = node_id

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(12, 6))
    labels = nx.get_node_attributes(G, 'label')

    nx.draw(G, pos, with_labels=False, node_size=2000, node_color="lightgreen", font_size=5, font_weight="bold")
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color="black", verticalalignment="center")

    plt.title("Connect Four Game Tree (Actual Moves)", fontsize=14)
    plt.axis('off')
    plt.show()
