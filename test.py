import tkinter as tk
import customtkinter as ctk

app = ctk.CTk()

container = tk.Frame(app)
container.pack(fill="both", expand=True)

canvas = tk.Canvas(container)
canvas.pack(side="left", fill="both", expand=True)

v_scroll = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
v_scroll.pack(side="right", fill="y")

h_scroll = tk.Scrollbar(app, orient="horizontal", command=canvas.xview)
h_scroll.pack(side="bottom", fill="x")

canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_configure)

# Add content
for i in range(20):
    for j in range(10):
        tk.Label(frame, text=f"{i},{j}", width=10).grid(row=i, column=j)

app.mainloop()