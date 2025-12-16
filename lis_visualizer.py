import tkinter as tk
from tkinter import messagebox

NODE_RADIUS = 16
LEVEL_GAP = 70
HORIZONTAL_GAP = 50
TOP_MARGIN = 40
LEFT_MARGIN = 60
ANIMATE_DELAY = 600

animation_job = None
animation_running = False
animation_index = 0
animation_steps = []
animation_positions = {}
animation_root_x = 0
current_arr = []
current_tree = {}
current_roots = []

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
        if not tree[node]:
            positions[key] = current_x[0]
            current_x[0] += HORIZONTAL_GAP
            return positions[key]

        child_x = []
        for c in tree[node]:
            child_x.append(dfs(c, level + 1, path + (node,)))

        positions[key] = sum(child_x) / len(child_x)
        return positions[key]

    for r in roots:
        dfs(r, 1, ())
    return positions

def draw_node(canvas, x, y, text, color="white"):
    canvas.create_oval(
        x - NODE_RADIUS, y - NODE_RADIUS,
        x + NODE_RADIUS, y + NODE_RADIUS,
        outline="black", width=2, fill=color
    )
    canvas.create_text(x, y, text=str(text), font=("Arial", 10, "bold"))

def stop_animation():
    global animation_running, animation_job
    animation_running = False
    if animation_job:
        root.after_cancel(animation_job)
        animation_job = None

def prepare_animation():
    global animation_steps, animation_positions, animation_index, animation_root_x
    animation_steps = []
    animation_index = 0

    animation_positions = calculate_tree_layout(current_arr, current_tree, current_roots)

    def dfs(node, level, path):
        animation_steps.append((path, node, level))
        for c in current_tree[node]:
            dfs(c, level + 1, path + (node,))

    for r in current_roots:
        dfs(r, 1, ())

    animation_root_x = sum(
        animation_positions[k] for k in animation_positions if k[2] == 1
    ) / len(current_roots)

    canvas.delete("all")
    draw_node(canvas, animation_root_x, TOP_MARGIN, "")

def play_animation():
    global animation_index, animation_running, animation_job

    if not animation_running or animation_index >= len(animation_steps):
        animation_running = False
        return

    path, idx, lvl = animation_steps[animation_index]
    x = animation_positions[(path, idx, lvl)]
    y = TOP_MARGIN + lvl * LEVEL_GAP

    if path:
        parent = path[-1]
        parent_key = (path[:-1], parent, lvl - 1)
        px = animation_positions[parent_key]
        py = TOP_MARGIN + (lvl - 1) * LEVEL_GAP
        canvas.create_line(px, py + NODE_RADIUS, x, y - NODE_RADIUS, fill="red", width=2)

    if lvl == 1:
        canvas.create_line(animation_root_x, TOP_MARGIN + NODE_RADIUS,
                           x, y - NODE_RADIUS, fill="red", width=2)

    draw_node(canvas, x, y, current_arr[idx], "#FFD966")

    animation_index += 1
    animation_job = root.after(ANIMATE_DELAY, play_animation)

def toggle_play():
    global animation_running
    if not animation_running:
        if animation_index == 0 or animation_index >= len(animation_steps):
            prepare_animation()
        animation_running = True
        play_animation()

def visualize_tree():
    global current_arr, current_tree, current_roots
    try:
        stop_animation()
        current_arr = list(map(int, entry.get().split()))
        if not current_arr:
            raise ValueError

        if mode_var.get() == "dag":
            current_tree = build_lis_tree(current_arr)
            current_roots = list(range(len(current_arr)))
        else:
            current_tree, current_roots, _ = build_pure_tree(current_arr)

        visualize_static()
    except:
        messagebox.showerror("Error", "Input tidak valid")

def visualize_static():
    canvas.delete("all")
    positions = calculate_tree_layout(current_arr, current_tree, current_roots)

    root_x = sum(positions[k] for k in positions if k[2] == 1) / len(current_roots)
    draw_node(canvas, root_x, TOP_MARGIN, "")

    for (path, idx, lvl), x in positions.items():
        y = TOP_MARGIN + lvl * LEVEL_GAP
        draw_node(canvas, x, y, current_arr[idx])

        if path:
            parent = path[-1]
            parent_key = (path[:-1], parent, lvl - 1)
            px = positions[parent_key]
            py = TOP_MARGIN + (lvl - 1) * LEVEL_GAP
            canvas.create_line(px, py + NODE_RADIUS, x, y - NODE_RADIUS, fill="gray", width=1.5)

        if lvl == 1:
            canvas.create_line(root_x, TOP_MARGIN + NODE_RADIUS,
                               x, y - NODE_RADIUS, fill="gray", width=1.5)

    lis_len = calculate_max_lis_length(current_arr, current_tree)
    info_label.config(text=f"Maximum LIS Length: {lis_len}")

    if mode_var.get() == "tree":
        teorema_label.config(text="Teorema 2-1: Terpenuhi", fg="green")
    else:
        teorema_label.config(text="Teorema 2-1: TIDAK Terpenuhi (DAG)", fg="red")

def clear_canvas():
    global animation_index, animation_steps, animation_running
    stop_animation()
    animation_index = 0
    animation_steps = []
    animation_running = False
    canvas.delete("all")
    info_label.config(text="—")
    teorema_label.config(text="Teorema 2-1: —", fg="black")

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
tk.Radiobutton(mode_frame, text="Mode PURE TREE", variable=mode_var, value="tree").pack(side="left", padx=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Visualisasikan",
          command=visualize_tree, bg="#4CAF50", fg="white", width=15).pack(side="left", padx=5)

tk.Button(btn_frame, text="Animate",
          command=toggle_play, bg="#2196F3", fg="white", width=15).pack(side="left", padx=5)

tk.Button(btn_frame, text="Clear",
          command=clear_canvas, bg="#F44336", fg="white", width=15).pack(side="left", padx=5)

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

info_label = tk.Label(root, text="—", font=("Arial", 11))
info_label.pack(pady=3)

teorema_label = tk.Label(root, text="Teorema 2-1: —", font=("Arial", 11, "bold"))
teorema_label.pack()

root.mainloop()
