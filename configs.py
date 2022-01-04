import tomlkit
from tomlkit.exceptions import TOMLKitError, ParseError
from tomlkit.toml_document import TOMLDocument
from pathlib import Path
from typing import Union

DEFAULT_CONFIGS_PATH = "configs.toml"

# TODO: lidiar con excepciones

def load_configs(f: Union[str, Path]) -> TOMLDocument:
    f = Path(f)
    data = tomlkit.loads(__default_configs)
    try:
        with f.open('r') as file:
            data = tomlkit.loads(file.read())
    except ParseError as e:
        print("Error al cargar configuración:")
        print(e)
        print("Cargando configuración por defecto.")
    except FileNotFoundError:
        print(f"El archivo {f} no existe.")
        print("Cargando configuración por defecto.")
    except PermissionError:
        print(f"No tiene permisos para abrir el archivo {f}")
        print("Cargando configuración por defecto.")

    return data


def save_configs(data: TOMLDocument, f: Union[str, Path]):
    f = Path(f)
    try:
        with f.open('w') as file:
            file.write(tomlkit.dumps(data))
    except TOMLKitError as e:
        print("Error al guardar configuración:")
        print(e)
        print("No se guardarán los cambios.")
    except PermissionError:
        print(f"No tiene permisos para abrir el archivo {f}")
        print("No se guardarán los cambios.")
    except OSError as e:
        print("Error al guardar configuración:")
        print(e)
        print("No se guardarán los cambios.")

        

__default_configs = """[tiempo]
fh_inicio = 2021-05-01T08:00:00 # YYYY-MM-DDThh:mm:ss
duracion_videos = 00:01:00 # hh:mm:ss
cantidad_videos = 2

[grabacion]
res_x = 640
res_y = 480
convert_mp4 = true

[preview]
on = false
fullscreen = false
pos_x = 0
pos_y = 0
scale = 3

[crop] # No está chequeado, mejor no utilizar
on = false
x = 0.0
y = 0.0
w = 1.0
h = 1.0
"""
