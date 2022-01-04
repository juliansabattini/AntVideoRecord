from configs import DEFAULT_CONFIGS_PATH, load_configs
import os
import sys
from glob import glob

import subprocess
from subprocess import check_output, CalledProcessError

import picamera
from picamera import PiCamera
import time
import threading
import datetime as dt
from datetime import datetime, date

import time
from time import sleep

import RPi.GPIO as GPIO

ErrorPin=13
RecLed=15
class Blinker:
    def __init__(self) -> None:
        self._rec_event = threading.Event()
        self._error_event = threading.Event()
        self._end_event = threading.Event()

        self._error_thread = threading.Thread(target=self._blink_error, args=(self._error_event, self._end_event))
        self._rec_thread = threading.Thread(target=self._blink_rec, args=(self._rec_event, self._end_event))

        self.start_rec = self._rec_event.set
        self.stop_rec = self._rec_event.clear
        self.error = self._error_event.set
        self.error_clear = self._error_event.clear

    def open(self):
        GPIO.setmode(GPIO.BOARD)            # Numbers GPIOs by physical location
        GPIO.setup(ErrorPin, GPIO.OUT)      # Set pin mode as output
        GPIO.output(ErrorPin, GPIO.LOW)    # Set pin low to turn on led
        GPIO.setup(RecLed, GPIO.OUT)      # Set pin mode as output
        GPIO.output(RecLed, GPIO.LOW)    # Set pin low to turn on led
        self._error_thread.start()
        self._rec_thread.start()

    def close(self):
        GPIO.cleanup()
        self._end_event.set()
        self._error_thread.join()
        self._rec_thread.join()

    @staticmethod
    def _blink_rec(rec: threading.Event, end: threading.Event):
        while not end.is_set():
            if rec.is_set():
                GPIO.output(RecLed, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(RecLed, GPIO.LOW)
                time.sleep(0.2)

    @staticmethod
    def _blink_error(error: threading.Event, end: threading.Event):
        while not end.is_set():
            if error.is_set():
                GPIO.output(ErrorPin, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(ErrorPin, GPIO.LOW)
                time.sleep(0.2)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

# DISPOSITIVOS USB

def get_usb_devices():
    sdb_devices = list(map(os.path.realpath, glob('/sys/block/sd*')))
    usb_devices = [dev for dev in sdb_devices
    	if any(('usb' in c) for c in dev.split('/'))]
    return dict((os.path.basename(dev), dev) for dev in usb_devices)

# DIRECCION DEL USB

def get_mount_points(devices=None, blinker: Blinker = None):
    devices = devices or get_usb_devices() # if devices are None: get_usb_devices
    output = check_output(['mount']).splitlines()
    output = [tmp.decode('UTF-8') for tmp in output]

    def is_usb(path):
        return any(dev in path for dev in devices)
    usb_info=(line for line in output if is_usb(line.split()[0]))
    #result=[(info.split()[0],info.split()[2]) for info in usb_info]
    result=[(info.split()[2]) for info in usb_info]
    
    if len(result):
        return result.pop()
    else:
        print('CONECTE UN DISPOSITIVO USB PARA GRABAR!' )
        blinker.error()

TFMT = "%H:%M:%S"

def hilo_convertir(videofile, blinker):
    vfname = os.path.split(videofile)[-1]
    print("(hilo_convertir)[{}] Comprimiendo en: {}".format(vfname, datetime.now().strftime(TFMT)))
    completed_video= os.path.join(get_mount_points(None, blinker), videofile)
    while not os.path.exists(completed_video):
        sleep(1)
        print("(hilo_convertir)[{}] Esperando que aparezca el .h264...".format(vfname))
    print("(hilo_convertir)[{}] Ejectuando FFMPEG".format(vfname))
    command = "ffmpeg -r 30 -i {} -vcodec copy {}.mp4; rm {}".format(completed_video, os.path.splitext(videofile)[0], completed_video)
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))
    print("(hilo_convertir)[{}] Compresión finalizada en: {}".format(vfname, datetime.now().strftime(TFMT))) 

def main(blinker: Blinker):
    completed=0
    #make destination direcory
    dstDir = get_mount_points(None, blinker)  + '/'
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)

    configs = load_configs(DEFAULT_CONFIGS_PATH)

    inicio = configs['tiempo']['fh_inicio']
    cant_videos = configs['tiempo']['cantidad_videos']
    _duracion = configs['tiempo']['duracion_videos']
    duracion = dt.timedelta(hours=_duracion.hour, minutes=_duracion.minute, seconds=_duracion.second)

    print("Esperando que llegue la hora de inicio...")
    while dt.datetime.now() < inicio:
        sleep(1)
    print("Comenzando...")
    hilos_convertir = []
    for _ in range(cant_videos):
        try:            
            res_x, res_y = (configs['grabacion']['res_x'], configs['grabacion']['res_y'])
            
            camera = PiCamera()
            camera.resolution = res_x, res_y
                #camera.sensor_mode = 1 
                #camera.framerate = 25
            if(configs['crop']['on']): # No está chequeado, mejor no usar
                crop_x = configs['crop']['x']
                crop_y = configs['crop']['y']
                crop_w = configs['crop']['w']
                crop_h = configs['crop']['h']
                print(f"MODO CROP: {crop_x}, {crop_y}, {crop_w}, {crop_h}")

                width  = res_x*crop_w
                height = res_y*crop_h

                percentAspectRatio = crop_w/crop_h  #Ratio in percent of size 
                imageAspectRatio   = width/height   #Desired aspect ratio
                sensorAspectRatio  = res_x/res_y    #Physical sensor aspect ratio

                #The sensor is automatically cropped to fit current aspect ratio 
                #so we need to adjust zoom to take that into account
                #if (imageAspectRatio > sensorAspectRatio):    
                #    crop_y = (crop_y - 0.5) * percentAspectRatio + 0.5  
                #    crop_h = crop_w                                  

                #if (imageAspectRatio < sensorAspectRatio):   
                #    crop_x = (crop_x - 0.5) * percentAspectRatio + 0.5  
                #    crop_w = crop_h 

                camera.zoom=(crop_x,crop_y,crop_w,crop_h)
                #camera.zoom=(crop_x2/res_x,crop_y2/res_y,crop_w2/res_x,crop_h2/res_y)
                #print("CROP DE ZOOM:"+str(crop_x/())+"XXX"+str(crop_y)+"XXX"+str(crop_w)+"XXX"+str(crop_h)+"XXX")

            preview = configs['preview']
            if preview['on']:
                if configs['crop']['on']:
                    camera.start_preview()
                elif preview['fullscreen']:
                    print(f"MODO FULL-SCREEN: {res_x}x{res_y}")
                    camera.start_preview(fullscreen=True)
                else:
                    print(f"MODO NO-FULL-SCREEN: {res_x}x{res_y}")
                    pos_x, pos_y = preview['pos_x'], preview['pos_y']
                    scale = preview['scale']
                    camera.start_preview(fullscreen=False, window=(pos_x, pos_y, res_x//scale, res_y//scale))

            start = dt.datetime.now()
            name = start.strftime("%Y-%m-%dT%H_%M_%S")
            print("El nombre del archivo va a ser: ", name)
            thisVideoFile = dstDir + name + '.h264'

            blinker.start_rec()
            print("Se empieza a grabar en: ", datetime.now().strftime(TFMT))
            camera.start_recording(thisVideoFile)
            while (dt.datetime.now() - start) < duracion:
                camera.wait_recording(.5)
            camera.stop_recording()
            camera.stop_preview()
            blinker.stop_rec()
            print("Se terminó de grabar en: ", datetime.now().strftime(TFMT))

            camera.close()

        except KeyboardInterrupt:
            print("terminando antes")
            camera.stop_recording()
            camera.stop_preview()
            blinker.stop_rec()
            print("Se terminó de grabar en: ", datetime.now().strftime(TFMT))
            camera.close()
            print("Camera stop recording")
            break

        if configs['grabacion']['convert_mp4']:
            hilo = threading.Thread(target=hilo_convertir, args=(thisVideoFile, blinker))
            hilos_convertir.append(hilo)
            hilo.start()

    for hilo in hilos_convertir:
        hilo.join()
    print("Grabación finalizada.")

if __name__ == "__main__":
    with Blinker() as blinker:
        main(blinker)
