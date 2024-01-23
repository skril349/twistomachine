import tkinter as tk
from PIL import Image, ImageTk
from screens.traction import create_screen as create_screen1
from screens.twist import create_screen as create_screen2
from screens.twistandtrac import create_screen as create_screen3

def toggle_fullscreen(root):
    state = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not state)

def main_window():
    root = tk.Tk()
    root.title("Pantalla Principal")
    
    # Obtiene las dimensiones de la pantalla actual
    screen_width = root.winfo_screenwidth() - 200
    screen_height = root.winfo_screenheight() -200

    # Establece la geometría de la ventana para que sea del tamaño de la pantalla
    root.geometry(f"{screen_width}x{screen_height}")

    # Crea una llista de funcions per a cada botó
    screen_functions = [create_screen1, create_screen2, create_screen3]

    for i, screen_function in enumerate(screen_functions):
        path = f'assets/image{i+1}.png'  # Actualitza el camí segons la ubicació de les teves imatges
        try:
            pil_image = Image.open(path)
            img = ImageTk.PhotoImage(pil_image)
            # Utilitza cada funció lambda amb la seva pròpia funció de pantalla
            btn = tk.Button(root, image=img, command=lambda screen_function=screen_function: screen_function(root, root.geometry()))
            btn.image = img  # Manté una referència!
            btn.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        except Exception as e:
            print(f"An error occurred: {e}")

    # Configurar un atajo de teclado para alternar el modo de pantalla completa (por ejemplo, F11)
    root.bind("<F11>", lambda event: toggle_fullscreen(root))

    root.mainloop()

# Això iniciarà l'aplicació en pantalla completa
main_window()
