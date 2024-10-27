import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BinaryTree:
    def __init__(self, size):
        self.tree = [None] * size
        self.size = size

    def insert(self, value):
        for i in range(self.size):
            if self.tree[i] is None:
                self.tree[i] = value
                return
        messagebox.showinfo("Info", "Tree is full, cannot insert more elements.")

    def delete(self, value):
        idx = self.search(value)
        if idx == -1:
            return  # Value not found

        left_child = 2 * idx + 1
        right_child = 2 * idx + 2

        if left_child >= self.size and right_child >= self.size:
            self.tree[idx] = None
        elif (left_child < self.size and self.tree[left_child] is not None) and (right_child >= self.size or self.tree[right_child] is None):
            self.tree[idx] = self.tree[left_child]
            self.tree[left_child] = None
        elif (right_child < self.size and self.tree[right_child] is not None) and (left_child >= self.size or self.tree[left_child] is None):
            self.tree[idx] = self.tree[right_child]
            self.tree[right_child] = None
        elif left_child < self.size and right_child < self.size:
            smallest = self._find_smallest(right_child)
            self.tree[idx] = self.tree[smallest]
            self.tree[smallest] = None

    def _find_smallest(self, index):
        current = index
        while 2 * current + 1 < self.size and self.tree[2 * current + 1] is not None:
            current = 2 * current + 1
        return current

    def search(self, value):
        return self.tree.index(value) if value in self.tree else -1

    def get_tree(self):
        return self.tree

    def infix_traversal(self, index=0, result=None):
        if result is None:
            result = []
        if index < self.size and self.tree[index] is not None:
            self.infix_traversal(2 * index + 1, result)
            result.append(self.tree[index])
            self.infix_traversal(2 * index + 2, result)
        return result

    def prefix_traversal(self, index=0, result=None):
        if result is None:
            result = []
        if index < self.size and self.tree[index] is not None:
            result.append(self.tree[index])
            self.prefix_traversal(2 * index + 1, result)
            self.prefix_traversal(2 * index + 2, result)
        return result

    def postfix_traversal(self, index=0, result=None):
        if result is None:
            result = []
        if index < self.size and self.tree[index] is not None:
            self.postfix_traversal(2 * index + 1, result)
            self.postfix_traversal(2 * index + 2, result)
            result.append(self.tree[index])
        return result

def visualize_tree(binary_tree, canvas_frame):
    G = nx.Graph()
    nodes = binary_tree.get_tree()
    edges = []
    positions = {}

    def add_edge_and_position(parent_idx, child_idx, direction):
        if nodes[child_idx] is not None or child_idx < len(nodes):
            edges.append((f"Node {parent_idx}", f"Node {child_idx}"))
            parent_pos = positions[f"Node {parent_idx}"]
            if direction == "left":
                child_pos = (parent_pos[0] - 2 ** (4 - parent_idx), parent_pos[1] - 1)
            elif direction == "right":
                child_pos = (parent_pos[0] + 2 ** (4 - parent_idx), parent_pos[1] - 1)
            positions[f"Node {child_idx}"] = child_pos

    if nodes[0] is not None or len(nodes) > 0:
        positions["Node 0"] = (0, 4)

    for idx, node in enumerate(nodes):
        left_child_idx = 2 * idx + 1
        right_child_idx = 2 * idx + 2
        if left_child_idx < len(nodes):
            add_edge_and_position(idx, left_child_idx, "left")
        if right_child_idx < len(nodes):
            add_edge_and_position(idx, right_child_idx, "right")

    G.add_edges_from(edges)

    fig, ax = plt.subplots(figsize=(10, 8))
    node_labels = {f"Node {i}": nodes[i] if nodes[i] is not None else "Empty" for i in range(len(nodes))}
    nx.draw(G, pos=positions, labels=node_labels, node_size=1500, node_color='skyblue',
            font_size=14, font_weight='bold', edge_color='gray', ax=ax)

    for widget in canvas_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

class BinaryTreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Tree Visualization")

        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.tree = None

        self.size_entry = self.create_entry(control_frame, "Tree Size:")
        self.value_entry = self.create_entry(control_frame, "Value(s):")

        self.create_button = tk.Button(control_frame, text="Create Tree", command=self.create_tree)
        self.create_button.pack(pady=5)

        self.insert_button = tk.Button(control_frame, text="Insert", command=self.insert_value)
        self.insert_button.pack(pady=5)

        self.delete_button = tk.Button(control_frame, text="Delete", command=self.delete_value)
        self.delete_button.pack(pady=5)

        self.traversal_frame = tk.Frame(control_frame)
        self.traversal_frame.pack(pady=10)

        self.infix_label = tk.Label(self.traversal_frame, text="Infix:")
        self.infix_label.grid(row=0, column=0, sticky="w")

        self.prefix_label = tk.Label(self.traversal_frame, text="Prefix:")
        self.prefix_label.grid(row=1, column=0, sticky="w")

        self.postfix_label = tk.Label(self.traversal_frame, text="Postfix:")
        self.postfix_label.grid(row=2, column=0, sticky="w")

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

    def create_entry(self, parent, label_text):
        frame = tk.Frame(parent)
        frame.pack(pady=5)
        label = tk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame)
        entry.pack(side=tk.RIGHT)
        return entry

    def create_tree(self):
        size = int(self.size_entry.get())
        self.tree = BinaryTree(size)
        self.update_visualization()

    def insert_value(self):
        values = map(int, self.value_entry.get().split())
        for value in values:
            self.tree.insert(value)
        self.update_visualization()

    def delete_value(self):
        value = int(self.value_entry.get())
        self.tree.delete(value)
        self.update_visualization()

    def update_visualization(self):
        if self.tree:
            self.canvas = visualize_tree(self.tree, self.canvas_frame)
            self.infix_label.config(text=f"Infix: {self.tree.infix_traversal()}")
            self.prefix_label.config(text=f"Prefix: {self.tree.prefix_traversal()}")
            self.postfix_label.config(text=f"Postfix: {self.tree.postfix_traversal()}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryTreeApp(root)
    root.mainloop()
