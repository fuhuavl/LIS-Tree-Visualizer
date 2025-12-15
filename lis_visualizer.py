import tkinter as tk
from tkinter import messagebox, ttk

NODE_RADIUS = 16
LEVEL_GAP = 70
HORIZONTAL_GAP = 50
TOP_MARGIN = 40
LEFT_MARGIN = 60

def build_lis_tree(arr):
    tree = {}
    n = len(arr)
    for i in range(n):
        tree[i] = []
        for j in range(i + 1, n):
            if arr[j] > arr[i]:
                tree[i].append(j)
    return tree

def build_pure_tree(arr):
    n = len(arr)
    dp = [1] * n
    parent = [-1] * n

    for i in range(n):
        for j in range(i):
            if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j

    tree = {i: [] for i in range(n)}
    roots = []

    for i in range(n):
        if parent[i] != -1:
            tree[parent[i]].append(i)
        else:
            roots.append(i)

    return tree, roots, dp

def calculate_max_lis_length(arr, tree):
    memo = {}

    def dp(idx):
        if idx in memo:
            return memo[idx]
        best = 1
        for child in tree[idx]:
            best = max(best, 1 + dp(child))
        memo[idx] = best
        return best

    return max(dp(i) for i in range(len(arr)))

def calculate_tree_layout(arr, tree, roots):
    positions = {}
    current_x = [LEFT_MARGIN]

    def dfs(node, level, path):
        key = (path, node, level)
        children = tree[node]

        if not children:
            x = current_x[0]
            positions[key] = x
            current_x[0] += HORIZONTAL_GAP
            return x

        child_x = []
        for c in children:
            new_path = path + (node,)
            child_x.append(dfs(c, level + 1, new_path))

        x = sum(child_x) / len(child_x)
        positions[key] = x
        return x

    for r in roots:
        dfs(r, 1, ())

    return positions

def draw_node(canvas, x, y, text):
    canvas.create_oval(
        x - NODE_RADIUS, y - NODE_RADIUS,
        x + NODE_RADIUS, y + NODE_RADIUS,
        outline="black", width=2, fill="white"
    )
    canvas.create_text(x, y, text=str(text), font=("Arial", 10, "bold"))

def visualize_complete_tree(canvas, arr, tree, roots):
    canvas.delete("all")
    positions = calculate_tree_layout(arr, tree, roots)

    root_x = sum(positions[k] for k in positions if k[2] == 1) / len(roots)
    draw_node(canvas, root_x, TOP_MARGIN, "")

    for (path, idx, lvl), x in positions.items():
        y = TOP_MARGIN + lvl * LEVEL_GAP
        draw_node(canvas, x, y, arr[idx])

        if path:
            parent = path[-1]
            parent_key = (path[:-1], parent, lvl - 1)
            px = positions[parent_key]
            py = TOP_MARGIN + (lvl - 1) * LEVEL_GAP
            canvas.create_line(px, py + NODE_RADIUS, x, y - NODE_RADIUS, fill="gray", width=1.5)

        if lvl == 1:
            canvas.create_line(root_x, TOP_MARGIN + NODE_RADIUS, x, y - NODE_RADIUS, fill="gray", width=1.5)

    return positions

def verify_teorema_2_1(tree):
    parent_count = {}
    for p in tree:
        for c in tree[p]:
            parent_count[c] = parent_count.get(c, 0) + 1
    return all(v <= 1 for v in parent_count.values())

def visualize_tree():
    try:
        arr = list(map(int, entry.get().split()))
        if not arr:
            raise ValueError

        if mode_var.get() == "dag":
            tree = build_lis_tree(arr)
            roots = list(range(len(arr)))
        else:
            tree, roots, _ = build_pure_tree(arr)

        visualize_complete_tree(canvas, arr, tree, roots)

        lis_len = calculate_max_lis_length(arr, tree)
        info_label.config(text=f"Maximum LIS Length: {lis_len}")

        if mode_var.get() == "tree":
            teorema_label.config(text="Teorema 2-1: Terpenuhi", fg="green")
        else:
            teorema_label.config(text="Teorema 2-1: TIDAK Terpenuhi (DAG)", fg="red")

    except:
        messagebox.showerror("Error", "Input tidak valid")

root = tk.Tk()
root.title("LIS Tree Visualizer")
root.geometry("1200x700")

tk.Label(root, text="Masukkan deret angka:", font=("Arial", 11)).pack()
entry = tk.Entry(root, width=60)
entry.pack()
entry.insert(0, "4 1 13 7 0 2 8 11 3")

mode_var = tk.StringVar(value="dag")
mode_frame = tk.Frame(root)
mode_frame.pack(pady=5)

tk.Radiobutton(mode_frame, text="Mode DAG", variable=mode_var, value="dag").pack(side="left", padx=10)
tk.Radiobutton(mode_frame, text="Mode PURE TREE (Teorema 2-1)", variable=mode_var, value="tree").pack(side="left", padx=10)

tk.Button(root, text="Visualisasikan", command=visualize_tree, bg="#4CAF50", fg="white").pack(pady=5)

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

info_label = tk.Label(root, text="—", font=("Arial", 11))
info_label.pack(pady=3)

teorema_label = tk.Label(root, text="Teorema 2-1: —", font=("Arial", 11, "bold"))
teorema_label.pack()

root.mainloop()
