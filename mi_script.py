# mi_script.py
import platform
import datetime

AUTOR = "José Miguel Blanco Vélez"  # Nombres completos del saludo y del README, en el mismo orden.

def main():
    print(f"Autor: {AUTOR}")
    print(f"Sistema Operativo: {platform.system()} {platform.release()}")
    print(f"Fecha y hora desde Python: {datetime.datetime.now()}")

if __name__ == "__main__":
    main()
