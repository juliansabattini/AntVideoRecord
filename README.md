# Ant Project

### CLONAR REPOSITORIO

*Desde la Rpi abrir la consola (Ctrl+Alt+T) y escribir:*
```
cd Desktop
git clone https://github.com/fd-sturniolo/ant_project
```
*Nota: Luego de clonar debe instalar las librerias y dependencias, ir a la sección de requisitos !!!*

### EJECUTAR LA APLICACION

*El archivo AntP (dentro de ant_project) es una acceso directo, por lo tanto puede moverlo al escritorio y ejecuta la aplicacion. Otra opción es es realizar:*
```
cd ant_project
python3 main_original.py
```

## REQUISITOS
### LIBRERIAS NECESARIAS
```
sudo apt-get install python3-pyqt5
sudo apt-get install python3-rpi.gpio
sudo apt install python3-smbus
pip3 install tomlkit
```

Si se clono el repositorio entrar a la carpeta ant_project (cd Desktop/ant_project) y ejecutar:
```
cd Adafruit_Python_DHT  
sudo python3 setup.py install 
```
*De otra manera realizar la instalacion de la libreria ADAFRUIT (pasos en LINK UTILES)*

### HABILITAR I2C
```
sudo raspi-config 
INTERFACE OPTIONS ---> SPI ---> yes
```

---

## LINKS UTILES PARA DESARROLLADORES
### LIBRERIA ADAFRUIT
```
mkdir -p /home/pi/sources  
cd /home/pi/sources  
git clone https://github.com/adafruit/Adafruit_Python_DHT.git  
cd Adafruit_Python_DHT  
sudo python setup.py install 
```

---

## Contribuciones 

* Cualquier consulta o mejora es bienvenida!
⌨️ [Martin Paz](https://github.com/freischarler) (martin.paz@live.com.ar) 
---

