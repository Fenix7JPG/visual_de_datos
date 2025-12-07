import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
def add_to_cart(pid):
    print("Agregado:", pid)

# ---------- Parámetros de diseño ----------
BTN_W = 180    # ancho fijo del botón contenedor (px)
BTN_H = 150    # alto fijo del botón contenedor (px)
PAD_X = 10     # espacio horizontal entre items
PAD_Y = 10     # espacio vertical entre items
LEFT_RIGHT_MARGIN = 16  # márgenes a restar del ancho usable
MARGIN = 16
# ---------- App ----------
root = tk.Tk()
root.title("Mallado con wrap - Pollería")
root.geometry("900x500")
root.minsize(MARGIN*2 + BTN_W * 2 + PAD_X * 4, 200)
main = ttk.Frame(root, padding=8)
main.pack(fill="both", expand=True)

canvas = tk.Canvas(main)
scroll_y = ttk.Scrollbar(main, orient="vertical", command=canvas.yview)
frame_container = ttk.Frame(canvas)
window_id = canvas.create_window((0,0), window=frame_container, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

# actualizar scrollregion cuando cambie el contenido
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
frame_container.bind("<Configure>", on_frame_configure)

# cuando cambia el ancho del canvas, ajustar el ancho interno y relayout
def on_canvas_configure(event):
    canvas.itemconfig(window_id, width=event.width)
    relayout_all(event.width)
canvas.bind("<Configure>", on_canvas_configure)

# carga simple de imagen (placeholder si no existe)
def load_image(path, size=(80, 80)):
    try:
        img = Image.open(path)
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        ph = tk.PhotoImage(width=size[0], height=size[1])
        return ph

# datos demo
CATEGORIES = [
    ("POLLO A LA BRASA", [
        {"id":101,"nombre":"Pollo entero","img":"imgs/1.png"},
        {"id":102,"nombre":"1/2 Pollo","img":"imgs/2.png"},
        {"id":103,"nombre":"Alitas","img":"imgs/3.png"},
        {"id":104,"nombre":"Pechuga","img":"imgs/1.png"},
        {"id":105,"nombre":"¼ Pollo","img":"imgs/2.png"},
    ]),
    ("GUARNICIONES", [
        {"id":201,"nombre":"Papas","img":"imgs/4.png"},
        {"id":202,"nombre":"Ensalada","img":"imgs/5.png"},
        {"id":203,"nombre":"Arroz","img":"imgs/6.png"},
        {"id":204,"nombre":"Yuca","img":"imgs/7.png"},
    ]),
    ("BEBIDAS", [
        {"id":401,"nombre":"Gaseosa","img":"imgs/10.png"},
        {"id":402,"nombre":"Agua","img":"imgs/11.png"},
    ]),
    ("EXTRAS", [
        {"id":501,"nombre":"Salsa extra","img":"imgs/12.png"},
        {"id":502,"nombre":"Papitas extra","img":"imgs/13.png"},
    ]),
]

# cache y estructura de categorías
_image_cache = {}
category_frames = []  # cada entry: {"frame": Frame, "items":[container,...]}

# construir UI: título, separador, frame por categoría y contenedores fijos por producto
row = 0
for cat_name, productos in CATEGORIES:
    lbl = ttk.Label(frame_container, text=cat_name, font=("Segoe UI", 13, "bold"))
    lbl.grid(row=row, column=0, sticky="w", pady=(12,6))
    row += 1
    ttk.Separator(frame_container, orient="horizontal").grid(row=row, column=0, sticky="ew", padx=2, pady=(0,6))
    row += 1

    products_frame = ttk.Frame(frame_container)
    products_frame.grid(row=row, column=0, sticky="ew", padx=2, pady=(0,8))
    info = {"products_frame": products_frame, "items": []}
    category_frames.append(info)

    for p in productos:
        key = p.get("img","")
        if key not in _image_cache: 
            _image_cache[key] = load_image(p.get("img",""))
        img = _image_cache[key]

        cont = ttk.Frame(products_frame, width=BTN_W, height=BTN_H, relief="flat")
        cont.pack_propagate(False)   # mantener tamaño fijo
        btn = ttk.Button(cont, text=p["nombre"], image=img, compound="top",
                         command=lambda pid=p["id"]: add_to_cart(pid))
        btn.pack(expand=True, fill="both")
        info["items"].append(cont)

    row += 1


def relayout_all(available_width):
    usable = max(50, available_width - MARGIN)
    step = BTN_W + PAD_X
    cols = max(1, usable // step)

    for info in category_frames:
        pf = info["products_frame"]
        # limpiar layout previo (pack forget)
        for w in pf.winfo_children():
            w.pack_forget()
        items = info["items"]

        for idx, cont in enumerate(items):
            r = idx // cols
            c = idx % cols

        # mejor: usar grid para pf (limpiar y regrid)
        for w in pf.winfo_children():
            w.grid_forget()
        for idx, cont in enumerate(items):
            r = idx // cols
            c = idx % cols

            cont.grid(row=r, column=c, padx=(PAD_X//2), pady=(PAD_Y//2))
        for c in range(cols):
            pf.grid_columnconfigure(c, weight=1)



initial_width = canvas.winfo_width() or root.winfo_width()
relayout_all(initial_width)

root.mainloop()
