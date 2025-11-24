import re

# Nombre del archivo de entrada y salida
INPUT_FILE = "lista_importada.txt"
OUTPUT_FILE = "lista_limpia.m3u"

def procesar_lista():
    print("Iniciando procesamiento de lista...")
    
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print("Error: No se encontró el archivo descargado.")
        return

    # Cabecera estándar para archivos m3u
    contenido_m3u = ["#EXTM3U"]
    contador_validos = 0

    # Expresión regular para capturar el nombre y el ID de 40 caracteres
    # Busca algo tipo: "Nombre del canal, acestream://123456..."
    # Ajusta esto según cómo venga tu lista exactamente. 
    # Asumimos formato simple o buscamos el patrón "acestream://"
    
    for linea in lineas:
        linea = linea.strip()
        if not linea: continue # Saltar líneas vacías
        
        # Buscamos el hash de 40 caracteres (letras a-f y números 0-9)
        match = re.search(r'acestream://([a-fA-F0-9]{40})', linea)
        
        if match:
            acestream_id = match.group(1)
            # Intentamos adivinar el nombre (todo lo que haya antes del enlace)
            nombre = linea.split("acestream://")[0].strip(" ,-:")
            if not nombre: nombre = "Canal Desconocido"
            
            # Creamos el formato M3U
            # #EXTINF:-1, Nombre del canal
            # acestream://id...
            contenido_m3u.append(f'#EXTINF:-1,{nombre}')
            contenido_m3u.append(f'acestream://{acestream_id}')
            contador_validos += 1
        else:
            print(f"Descartado (formato inválido): {linea}")

    # Guardamos el nuevo archivo
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(contenido_m3u))
    
    print(f"Proceso terminado. Se encontraron {contador_validos} canales válidos.")

if __name__ == "__main__":
    procesar_lista()
