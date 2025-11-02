import tkinter as tk
from interface import OcorrenciasApp

def main():
    root = tk.Tk()
    app = OcorrenciasApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()