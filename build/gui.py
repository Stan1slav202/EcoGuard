from pathlib import Path
from tkinter import Tk, Canvas, Frame, Scrollbar, Button, PhotoImage, Entry, Toplevel, VERTICAL, HORIZONTAL, Label

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\\Users\\uyinc\\Downloads\\14\\build\\assets\\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.title("EcoGuard Calculator")
window.geometry("1000x700")
window.configure(bg="#FFFFFF")
window.iconbitmap(r"C:\Users\uyinc\Downloads\14\build\assets\frame0\ico.ico")

# Funcție pentru a centra fereastra pe ecran
def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

# Centrarea ferestrei principale
center_window(window, 1000, 700)

# Panou de sus (fără scroll)
top_frame = Frame(window, bg="#FFFFFF", height=138)
top_frame.pack(side="top", fill="x")

# Panou turcoaz (parte din top_frame)
header_canvas = Canvas(
    top_frame,
    bg="#38C2A5",  # Culoare turcoaz
    height=138,
    width=1000,
    bd=0,
    highlightthickness=0
)
header_canvas.pack(side="top", fill="x")
image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
header_canvas.create_image(500.0, 69.0, image=image_image_3)

# Butoane din panoul de sus
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    top_frame,
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(x=871, y=15, width=49.0, height=49.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    top_frame,
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(x=737, y=15, width=49.0, height=49.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    top_frame,
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Add Tile clicked"),
    relief="flat"
)
button_2.place(x=804, y=15, width=49.0, height=49.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    top_frame,
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=window.quit,
    relief="flat"
)
button_3.place(x=938, y=15, width=49, height=49)

# Partea scrollabilă
scroll_frame = Frame(window)
scroll_frame.pack(side="bottom", fill="both", expand=True)

# Adăugăm bare de scroll
v_scrollbar = Scrollbar(scroll_frame, orient=VERTICAL)
h_scrollbar = Scrollbar(scroll_frame, orient=HORIZONTAL)

canvas = Canvas(
    scroll_frame,
    bg="#F0F0F0",
    yscrollcommand=v_scrollbar.set,
    xscrollcommand=h_scrollbar.set
)
canvas.pack(side="left", fill="both", expand=True)

v_scrollbar.config(command=canvas.yview)
h_scrollbar.config(command=canvas.xview)

# Ascundem barele de scroll inițial
v_scrollbar.pack_forget()
h_scrollbar.pack_forget()

# Configurăm zona scrollabilă
canvas.configure(scrollregion=(0, 0, 1500, 1000))  # Dimensiunea zonei scrollabile

# Parametri pentru plasarea tile-urilor
tile_size = 150
tile_spacing_long = 45
tile_spacing_down = 105
tiles_per_row = 5
current_tile_count = 0
image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))

# Liste pentru stocarea valorilor
denumire_list = []  # Lista denumirilor
consum_list = []  # Lista valorilor de consum
hours_list = []  # Lista orelor

# Liste pentru stocarea referințelor câmpurilor de introducere
entry_denumire_list = []
entry_consum_list = []
entry_hours_list = []

# Funcție pentru validarea introducerii doar de cifre
def validate_number(P):
    return P.isdigit() or P == ""

# Funcție pentru adăugarea de tile-uri
def add_tile():
    global current_tile_count

    # Calculăm poziția tile-ului
    row = current_tile_count // tiles_per_row
    col = current_tile_count % tiles_per_row

    x = 110 + col * (tile_size + tile_spacing_long)
    y = 130 + row * (tile_size + tile_spacing_down)

    # Adăugăm tile-ul pe canvas
    canvas.create_image(x, y, image=image_image_2)

    # Cream valori inițiale pentru noul tile
    denumire_list.append("")  # Denumire goală
    consum_list.append("")  # Consum gol
    hours_list.append("")  # Ore goale

    # Cream câmpuri de introducere
    entry_denumire = Entry(canvas, width=15)
    entry_consum = Entry(canvas, width=10, validate="key", validatecommand=(vcmd, "%P"))
    entry_hours = Entry(canvas, width=10, validate="key", validatecommand=(vcmd, "%P"))

    # Adăugăm câmpurile de introducere în liste
    entry_denumire_list.append(entry_denumire)
    entry_consum_list.append(entry_consum)
    entry_hours_list.append(entry_hours)

    # Plasăm câmpurile de introducere
    canvas.create_window(x - 3, y + 45, window=entry_denumire)
    canvas.create_window(x - 3, y + 70, window=entry_consum)
    canvas.create_window(x - 3, y + 95, window=entry_hours)

    # Creștem contorul de tile-uri
    current_tile_count += 1

    # Actualizăm zona scrollabilă dacă este necesar
    canvas.configure(scrollregion=canvas.bbox("all"))
    update_scrollbars()

# Funcție pentru procesarea și afișarea datelor
def process_and_display():
    # Actualizăm listele cu valori înainte de calcul
    for i in range(len(entry_denumire_list)):
        denumire_list[i] = entry_denumire_list[i].get()
        consum_list[i] = entry_consum_list[i].get()
        hours_list[i] = entry_hours_list[i].get()

    # Efectuăm calculul
    try:
        total_consum = sum(float(consum) for consum in consum_list if consum)
        total_hours = sum(float(hours) for hours in hours_list if hours)
        energy = (total_consum * total_hours) / 1000
        money = energy * 4.2
        # Afișăm rezultatul în colțul din stânga sus
        header_canvas.delete("result_text")  # Ștergem rezultatul anterior dacă există
        header_canvas.create_text(
            30, 25, anchor="nw", text=f"Energie economisită {energy:.2f} kW" "\n" f"Bani economisiţi {money:.2f} lei", fill="#000000", font=("Franklin Gothic Medium", 13, "bold"), tags="result_text"
        )
    except ValueError:
        print("Date greșite în consum_list sau hours_list")

# Atribuim funcțiile butoanelor
button_2.configure(command=add_tile)
button_4.configure(command=process_and_display)

# Actualizăm starea barurilor de scroll
def update_scrollbars():
    canvas.update_idletasks()
    canvas_bbox = canvas.bbox("all")
    if canvas_bbox[2] > canvas.winfo_width():
        h_scrollbar.pack(side="bottom", fill="x")
    else:
        h_scrollbar.pack_forget()
    if canvas_bbox[3] > canvas.winfo_height():
        v_scrollbar.pack(side="right", fill="y")
    else:
        v_scrollbar.pack_forget()

# Configurăm validarea pentru câmpurile de introducere
vcmd = window.register(validate_number)

# Funcție pentru deschiderea unei ferestre noi
def open_new_window():
    # Ascundem fereastra principală
    window.withdraw()

    # Cream o fereastră nouă
    new_window = Toplevel(window)  # Specificăm fereastra principală ca părinte
    new_window.title("EcoGuard Cabinet")
    new_window.iconbitmap(r"C:\Users\uyinc\Downloads\14\build\assets\frame0\ico.ico")
    new_window.geometry("1000x700")
    new_window.configure(bg="#FFFFFF")
    new_window.resizable(False, False)

    # Centrarea ferestrei noi
    center_window(new_window, 1000, 700)

    # Încărcăm imaginea de fundal
    image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))

    # Cream Canvas pentru fereastra nouă
    new_canvas = Canvas(new_window, width=1000, height=700, bg="#FFFFFF", highlightthickness=0)
    new_canvas.pack(fill="both", expand=True)

    # Afișăm imaginea de fundal
    new_canvas.create_image(500, 350, image=image_image_4)

    # Încărcăm iconița pentru butonul de întoarcere
    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))

    # Buton pentru întoarcerea la fereastra principală
    return_button = Button(
        new_window,
        image=button_image_5,  # Setăm iconița
        command=lambda: close_new_window(new_window),  # Închide fereastra nouă și revine la cea principală
        bg="#FFFFFF",
        borderwidth=0,
        highlightthickness=0,
        relief="flat"
    )
    return_button.place(x=16, y=8, width=49, height=49)  # Dimensiunea butonului depinde de iconiță

    # Salvăm referințele pentru imagini pentru a preveni ștergerea acestora de garbage collector
    new_window.image_image_4 = image_image_4
    new_window.return_button_icon = button_image_5

# Funcție pentru închiderea noii ferestre și revenirea la cea principală
def close_new_window(new_window):
    new_window.destroy()  # Închidem fereastra nouă
    window.deiconify()  # Afișăm din nou fereastra principală
    center_window(window, 1000, 700)  # Centrăm din nou fereastra principală

# Atribuim funcția butonului
button_1.configure(command=open_new_window)

window.resizable(False, False)
window.mainloop()
