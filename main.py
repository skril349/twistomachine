import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

def create_window(root, window_number, window_geometry):
    # Amagar la finestra principal
    root.withdraw()
    
    window = tk.Toplevel()
    window.title(f'Pantalla {window_number}')
    window.geometry(window_geometry)  # Definir la geometria de la finestra secundària
    
    label = tk.Label(window, text=f"Aquesta és la pantalla {window_number}")
    label.pack(side="top", fill="both", padx=20, pady=20)
    
    btn_back = tk.Button(window, text="Torna enrere", command=lambda: close_window(root, window))
    btn_back.pack(side="bottom", pady=20)

def close_window(root, window):
    window.destroy()
    root.deiconify()

def main_window():
    root = tk.Tk()
    root.title("Pantalla Principal")

    # Definir el tamany i posició de la finestra principal
    window_geometry = "800x600+100+100"  # Exemple: 600x400 és el tamany, 100+100 és la posició
    root.geometry(window_geometry)

    for i in range(1, 4):
        path = f'assets/image{i}.png'
        try:
            pil_image = Image.open(path)
            img = ImageTk.PhotoImage(pil_image)
            btn = tk.Button(root, image=img, command=lambda i=i: create_window(root, i, window_geometry))
            btn.image = img  # keep a reference!
            btn.pack(side="left", padx=10, pady=10)
        except Exception as e:
            print(f"An error occurred: {e}")

    root.mainloop()

# Això iniciarà l'aplicació
main_window()
