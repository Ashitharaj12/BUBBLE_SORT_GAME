import tkinter as tk
import time
import random

# ---------------- WINDOW ----------------
window = tk.Tk()
window.title("Ball Sorting Game (Wavelength Based)")
window.geometry("800x560")
window.configure(bg="#1e272e")
window.resizable(False, False)

# ---------------- TITLE ----------------
tk.Label(
    window,
    text="🎮 Ball Sorting Game (Color by Wavelength)",
    font=("Segoe UI", 18, "bold"),
    bg="#1e272e",
    fg="#feca57"
).pack(pady=12)

# ---------------- USER INFO (TOP RIGHT) ----------------
user_info = tk.Label(
    window,
    text="Ashitha Rajagopal\nUSN: 25MCAR0239",
    font=("Segoe UI", 10, "bold"),
    bg="#1e272e",
    fg="#dfe6e9",
    justify="right"
)
user_info.place(x=790, y=10, anchor="ne")

# ---------------- CANVAS ----------------
canvas_frame = tk.Frame(window, bg="#485460", bd=4, relief="ridge")
canvas_frame.pack(pady=10)

canvas = tk.Canvas(
    canvas_frame,
    width=720,
    height=320,
    bg="#f5f6fa",
    highlightthickness=0
)
canvas.pack(padx=12, pady=12)

# ---------------- DATA ----------------
COLORS = ["red", "orange", "yellow", "green", "blue", "violet"]

# wavelength priority (long → short)
color_wavelength = {
    "red": 700,
    "orange": 620,
    "yellow": 580,
    "green": 530,
    "blue": 470,
    "violet": 420
}

balls = []
ball_data = []

START_X = 60
GAP = 110
BASE_Y = 240

# ---------------- RANDOM BALLS ----------------
def generate_random_balls():
    canvas.delete("all")
    balls.clear()
    ball_data.clear()

    sizes = random.sample(range(35, 70), 6)
    random.shuffle(COLORS)

    for i in range(6):
        size = sizes[i]
        color = COLORS[i]

        x = START_X + i * GAP
        y = BASE_Y - size

        shadow = canvas.create_oval(
            x + 6, y + size + 8,
            x + size + 6, y + size + 16,
            fill="#b2bec3",
            outline=""
        )

        ball = canvas.create_oval(
            x, y,
            x + size, y + size,
            fill=color,
            outline="#2d3436",
            width=2
        )

        balls.append((ball, shadow))
        ball_data.append({
            "color": color,
            "size": size
        })

# ---------------- ANIMATION ----------------
def animate_swap(i, j):
    steps = 30
    dx = GAP / steps

    for _ in range(steps):
        for obj in balls[i]:
            canvas.move(obj, dx, 0)
        for obj in balls[j]:
            canvas.move(obj, -dx, 0)
        window.update()
        time.sleep(0.015)

    balls[i], balls[j] = balls[j], balls[i]
    ball_data[i], ball_data[j] = ball_data[j], ball_data[i]

# ---------------- SORTING ----------------
def bubble_sort(mode):
    status_label.config(text=f"🔄 Sorting by {mode}...", fg="#feca57")

    n = len(balls)
    for i in range(n):
        for j in range(n - i - 1):

            b1 = balls[j][0]
            b2 = balls[j + 1][0]

            canvas.itemconfig(b1, outline="#0984e3", width=4)
            canvas.itemconfig(b2, outline="#0984e3", width=4)
            window.update()
            time.sleep(0.2)

            if mode == "Color":
                condition = (
                    color_wavelength[ball_data[j]["color"]]
                    < color_wavelength[ball_data[j + 1]["color"]]
                )
            else:  # Size
                condition = ball_data[j]["size"] > ball_data[j + 1]["size"]

            if condition:
                canvas.itemconfig(b1, outline="#d63031")
                canvas.itemconfig(b2, outline="#d63031")
                window.update()
                time.sleep(0.2)
                animate_swap(j, j + 1)

            canvas.itemconfig(b1, outline="#2d3436", width=2)
            canvas.itemconfig(b2, outline="#2d3436", width=2)

    status_label.config(text="✅ Sorting Completed!", fg="#00b894")

# ---------------- BUTTONS ----------------
btn_frame = tk.Frame(window, bg="#1e272e")
btn_frame.pack(pady=18)

tk.Button(
    btn_frame,
    text="🌈 Arrange by Wavelength",
    font=("Segoe UI", 13, "bold"),
    bg="#27ae60",
    fg="white",
    width=22,
    relief="flat",
    command=lambda: bubble_sort("Color")
).grid(row=0, column=0, padx=12)

tk.Button(
    btn_frame,
    text="📏 Arrange by Size",
    font=("Segoe UI", 13, "bold"),
    bg="#0984e3",
    fg="white",
    width=18,
    relief="flat",
    command=lambda: bubble_sort("Size")
).grid(row=0, column=1, padx=12)

tk.Button(
    btn_frame,
    text="⟲ Reset (Random)",
    font=("Segoe UI", 13, "bold"),
    bg="#c0392b",
    fg="white",
    width=16,
    relief="flat",
    command=generate_random_balls
).grid(row=0, column=2, padx=12)

# ---------------- STATUS ----------------
status_label = tk.Label(
    window,
    text="Click a sorting option to start",
    font=("Segoe UI", 11),
    bg="#1e272e",
    fg="white"
)
status_label.pack()

# ---------------- START ----------------
generate_random_balls()
window.mainloop()
