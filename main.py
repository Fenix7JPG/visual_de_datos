import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

def calcular_total():
    total = 0.0
    for item in carrito.get_children():
        vals = carrito.item(item, "values")
        print(vals)
        # vals = (id, nombre, cantidad, subtotal)
        subtotal = float(vals[3])
        total += subtotal
    return round(total, 2)
def añadir_al_carrito(pid):
    prod = PRODUCT_MAP.get(pid)
    nombre = prod.get("nombre")
    precio = prod.get("precio")

    for item in carrito.get_children():
        vals = carrito.item(item, "values")
        if int(vals[0]) == pid:
            nueva_cant = int(vals[2]) + 1
            nuevo_precio = round(nueva_cant * precio, 2)
            carrito.item(item, values=(pid, nombre, nueva_cant, nuevo_precio))
            label_total.config(text=f"Total: S/ {calcular_total()}")
            return

    # no existe -> insertar nuevo (cantidad 1)
    carrito.insert("", "end", values=(pid, nombre, 1, f"{precio}"))


    label_total.config(text=f"Total: S/ {calcular_total()}")
# ---------- App ----------
root = tk.Tk()
root.title("Mallado con wrap - Pollería")
root.geometry("900x500")
root.minsize(600, 200)
main = ttk.Frame(root, padding=4)
main.pack(fill="both", expand=True)

# === CARRITO ===
carrito_frame = ttk.Frame(main,relief="groove")
carrito_frame.pack(side="left", fill="y", padx=10, pady=4)

ttk.Label(carrito_frame, text="CARRITO", font=("Segoe UI", 14, "bold")).pack(pady=5)
carrito = ttk.Treeview(
    carrito_frame,
    columns=("id", "nombre", "cant", "precio"),
    show="headings",
)

carrito.heading("id", text="ID")
carrito.heading("nombre", text="Nombre")
carrito.heading("cant", text="Cant.")
carrito.heading("precio", text="Precio")

carrito.column("id", width=40, anchor="center")
carrito.column("nombre", width=140)
carrito.column("cant", width=50, anchor="center")
carrito.column("precio", width=60, anchor="e")

carrito.pack(fill="both", expand=True, pady=5,padx=5)


bottom_box = ttk.Frame(carrito_frame, padding=4)
bottom_box.pack(side="bottom", fill="x", pady=2,padx=2)

# --- GRID dentro de bottom_box ---
bottom_box.columnconfigure(0, weight=1)   # columna izquierda
bottom_box.columnconfigure(1, weight=1)   # columna centro
bottom_box.columnconfigure(2, weight=1)   # columna derecha

# Total → derecha
label_total = ttk.Label(bottom_box, text="Total: S/ 0.00")
label_total.grid(row=0, column=2, sticky="e")

# Botón → centro
btn_finalizar = ttk.Button(bottom_box, text="Finalizar Pedido")
btn_finalizar.grid(row=1, column=1)

######################


# ======= SELECCION DE PRODUCTOS ==============
canvas = tk.Canvas(main, bd=0, highlightthickness=0, relief="flat", background="white")
scroll_y = ttk.Scrollbar(main, orient="vertical", command=canvas.yview)
productos_frame = ttk.Frame(canvas, relief="groove")

window_id = canvas.create_window((0,0), window=productos_frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

canvas.pack(side="left", fill="both", expand=True,pady=4)
scroll_y.pack(side="left", fill="y")


# datos
CATEGORIES = [
    ("POLLO A LA BRASA", [
        {"id":101,"nombre":"Pollo entero","img":"imgs/1.png","precio":28.00},
        {"id":102,"nombre":"1/2 Pollo","img":"imgs/2.png","precio":16.00},
        {"id":103,"nombre":"Alitas","img":"imgs/3.png","precio":12.00},
        {"id":104,"nombre":"Pechuga","img":"imgs/1.png","precio":14.00},
        {"id":105,"nombre":"¼ Pollo","img":"imgs/2.png","precio":9.00},
    ]),
    ("GUARNICIONES", [
        {"id":201,"nombre":"Papas","img":"imgs/4.png","precio":6.50},
        {"id":202,"nombre":"Ensalada","img":"imgs/5.png","precio":5.00},
        {"id":203,"nombre":"Arroz","img":"imgs/6.png","precio":4.50},
        {"id":204,"nombre":"Yuca","img":"imgs/7.png","precio":6.00},
    ]),
    ("BEBIDAS", [
        {"id":401,"nombre":"Gaseosa","img":"imgs/10.png","precio":7.00},
        {"id":402,"nombre":"Agua","img":"imgs/11.png","precio":3.00},
    ]),
    ("EXTRAS", [
        {"id":501,"nombre":"Salsa extra","img":"imgs/12.png","precio":0.50},
        {"id":502,"nombre":"Papitas extra","img":"imgs/13.png","precio":3.00},
    ]),
]


PRODUCT_MAP = {}
for cat_name, productos in CATEGORIES:
    for p in productos:
        PRODUCT_MAP[p["id"]] = p

# cache y estructura de categorías
_image_cache = {}
category_frames = []

row = 0

# carga simple de imagen (placeholder si no existe)
def load_image(path, size=(80, 80)):
    try:
        img = Image.open(path)
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        ph = tk.PhotoImage(width=size[0], height=size[1])
        return ph


BTN_W = 180
BTN_H = 150
PAD_X = 10
PAD_Y = 10
MARGIN = 16
for cat_name, productos in CATEGORIES:
    lbl = ttk.Label(productos_frame, text=cat_name, font=("Segoe UI", 13, "bold"))
    lbl.grid(row=row, column=0, sticky="w", pady=6,padx=10)
    row += 1
    ttk.Separator(productos_frame, orient="horizontal").grid(row=row, column=0, sticky="ew", padx=2, pady=(0,6))
    row += 1

    products_frame = ttk.Frame(productos_frame)
    products_frame.grid(row=row, column=0, sticky="ew", padx=2, pady=(0,8))
    info = {"products_frame": products_frame, "items": []}
    category_frames.append(info)

    for p in productos:
        key = p.get("img","")
        if key not in _image_cache: 
            _image_cache[key] = load_image(p.get("img",""))
        img = _image_cache[key]

        cont = ttk.Frame(products_frame, width=BTN_W, height=BTN_H)
        cont.pack_propagate(False)
        btn = ttk.Button(cont, text=p["nombre"], image=img, compound="top",
                         command=lambda pid=p["id"]: añadir_al_carrito(pid))
        btn.pack(expand=True, fill="both")
        info["items"].append(cont)

    row += 1

########################



# actualizar scrollregion cuando cambie el contenido
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
productos_frame.bind("<Configure>", on_frame_configure)

# cuando cambia el ancho del canvas, ajustar el ancho interno y relayout
def on_canvas_configure(event):
    canvas.itemconfig(window_id, width=event.width)
    relayout_all(event.width)
canvas.bind("<Configure>", on_canvas_configure)


def relayout_all(available_width):
    usable = max(50, available_width - MARGIN)
    step = BTN_W + PAD_X
    cols = max(1, usable // step)

    for info in category_frames:
        pf = info["products_frame"]

        for w in pf.winfo_children():
            w.grid_forget()

        items = info["items"]

        for idx, cont in enumerate(items):
            r = idx // cols
            c = idx % cols
            cont.grid(row=r, column=c, padx=PAD_X, pady=PAD_Y)

        for c in range(cols):
            pf.grid_columnconfigure(c, weight=1)

root.mainloop()
