import tkinter as tk
from PIL import Image, ImageTk
from screens.traction import create_screen as create_screen1
from screens.twist import create_screen as create_screen2
from screens.twistandtrac import create_screen as create_screen3
from Odrive.odrive_setup import setup_odrive as setup_odrive
import sys

def toggle_fullscreen(root):
    state = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not state)

def close_application(root):
    # Cierra la ventana y termina la ejecución del programa
    root.destroy()
    sys.exit()

def main_window():
    root = tk.Tk()
    root.title("Pantalla Principal")
    
    # Obtiene las dimensiones de la pantalla actual
    screen_width = root.winfo_screenwidth() - 200
    screen_height = root.winfo_screenheight() - 200

    # Establece la geometría de la ventana para que sea del tamaño de la pantalla
    root.geometry(f"{screen_width}x{screen_height}")

    # Crea una lista de funciones para cada botón
    screen_functions = [create_screen1, create_screen2, create_screen3]

    for i, screen_function in enumerate(screen_functions):
        path = f'assets/image{i+1}.png'  # Actualiza el camino según la ubicación de tus imágenes
        try:
            pil_image = Image.open(path)
            img = ImageTk.PhotoImage(pil_image)
            # Utiliza cada función lambda con su propia función de pantalla
            

            btn = tk.Button(root, image=img, command=lambda screen_function=screen_function: screen_function(root, root.geometry()))
            btn.image = img  # Mantiene una referencia!
            btn.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            if i == 0 or i == 2:
                btn['state'] = 'disabled'
        except Exception as e:
            print(f"An error occurred: {e}")

    # Configura un atajo de teclado para alternar el modo de pantalla completa (por ejemplo, F11)
    root.bind("<F11>", lambda event: toggle_fullscreen(root))

    # Cierra la aplicación y la terminal cuando se cierra la ventana principal
    root.protocol("WM_DELETE_WINDOW", lambda: close_application(root))

    root.mainloop()

if __name__ == "__main__":
    setup_odrive()  # Configura ODrive
    main_window()  # Inicia la ventana principal
