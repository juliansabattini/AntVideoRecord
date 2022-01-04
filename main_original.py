from configs import DEFAULT_CONFIGS_PATH, load_configs, save_configs
import sys
import os


import subprocess
from subprocess import Popen, PIPE

import threading
from random import random

import picamera
from picamera import PiCamera
from time import sleep
import datetime as dt

import smbus #para i2c

from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QAction

import Adafruit_DHT
# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT22
 
# Set GPIO sensor is connected to
temp_gpio=20
uv_gpio=0


# Define some constants from the datasheet
DEVICE     = 0x23 # Default device I2C address
POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value
ONE_TIME_HIGH_RES_MODE = 0x20

bus = smbus.SMBus(1)
def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number
    return ((data[1] + (256 * data[0])) / 1.2)

def readLight(addr=DEVICE):
    data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE)
    return convertToNumber(data)

    #-----------------------------
    #   VENTANA DE CONFIGURACION DE PANTALLA
    #-----------------------------
    
class Ui_ConfigurarPantalla(object):
    tiempo_finalizacion=0
    duracion_grabacion=0
    cantidad_videos=0
    resolucion_x=640
    resolucion_y=480
    comprimir="no"

    f_actual="1/1/00"
    h_actual="12:12"
    tiempo_defecto="yes"
    h_inicio="13:13"
    duracion_videos=15
    cantidad_videos=1



    resize=1
    


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 391)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(190, 350, 341, 32))
        font = QtGui.QFont()
        font.setKerning(True)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(20, 10, 601, 331))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(80, 20, 230, 241))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        self.le_fecha = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        self.le_fecha.setObjectName("le_fecha")
        self.horizontalLayout_3.addWidget(self.le_fecha)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_14 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_7.addWidget(self.label_14)
        self.le_hora = QtWidgets.QTimeEdit(self.verticalLayoutWidget)
        self.le_hora.setObjectName("le_hora")
        self.horizontalLayout_7.addWidget(self.le_hora)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.btn_tiempo_default = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_tiempo_default.setObjectName("btn_tiempo_default")
        self.verticalLayout.addWidget(self.btn_tiempo_default)

        self.le_iniciofecha_hl = QtWidgets.QHBoxLayout()
        self.le_iniciofecha_hl.setObjectName("le_iniciofecha_hl")
        self.le_iniciofecha_lbl = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.le_iniciofecha_lbl.setObjectName("le_iniciofecha_lbl")
        self.le_iniciofecha = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        self.le_iniciofecha.setObjectName("le_iniciofecha")
        self.le_iniciofecha_hl.addWidget(self.le_iniciofecha_lbl)
        self.le_iniciofecha_hl.addWidget(self.le_iniciofecha)
        
        self.le_inicio_hl = QtWidgets.QHBoxLayout()
        self.le_inicio_hl.setObjectName("le_inicio_hl")
        self.le_inicio_lbl = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.le_inicio_lbl.setObjectName("le_inicio_lbl")
        self.le_inicio = QtWidgets.QTimeEdit(self.verticalLayoutWidget)
        self.le_inicio.setObjectName("le_inicio")
        self.le_inicio_hl.addWidget(self.le_inicio_lbl)
        self.le_inicio_hl.addWidget(self.le_inicio)

        self.verticalLayout.addLayout(self.le_iniciofecha_hl)
        self.verticalLayout.addLayout(self.le_inicio_hl)

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.le_duracion = QtWidgets.QTimeEdit(self.verticalLayoutWidget)
        self.le_duracion.setTimeRange(QTime(0,0,5), QTime(23,59,59))    
        self.le_duracion.setDisplayFormat("HH:mm:ss")
        self.le_duracion.setObjectName("le_duracion")
        self.horizontalLayout_6.addWidget(self.le_duracion)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.le_cantidad = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.le_cantidad.setRange(1, 99999) # TODO: cambiar este campo a "hora de finalización" 
        self.le_cantidad.setObjectName("le_cantidad")
        self.horizontalLayout.addWidget(self.le_cantidad)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_21 = QtWidgets.QLabel(self.tab)
        self.label_21.setGeometry(QtCore.QRect(310, 30, 241, 101))
        self.label_21.setObjectName("label_21")
        self.tabWidget.addTab(self.tab, "")
        self.Video = QtWidgets.QWidget()
        self.Video.setObjectName("Video")
        self.label_7 = QtWidgets.QLabel(self.Video)
        self.label_7.setGeometry(QtCore.QRect(99, 40, 125, 33))
        self.label_7.setObjectName("label_7")
        self.qbox_resolucion = QtWidgets.QComboBox(self.Video)
        self.qbox_resolucion.setGeometry(QtCore.QRect(230, 40, 124, 25))
        self.qbox_resolucion.setObjectName("qbox_resolucion")
        self.checkBox_convertir = QtWidgets.QCheckBox(self.Video)
        self.checkBox_convertir.setGeometry(QtCore.QRect(100, 120, 311, 23))
        self.checkBox_convertir.setObjectName("checkBox_convertir")
        self.label_19 = QtWidgets.QLabel(self.Video)
        self.label_19.setGeometry(QtCore.QRect(100, 160, 321, 17))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.Video)
        self.label_20.setGeometry(QtCore.QRect(100, 80, 441, 17))
        self.label_20.setObjectName("label_20")
        self.tabWidget.addTab(self.Video, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.line = QtWidgets.QFrame(self.tab_3)
        self.line.setGeometry(QtCore.QRect(50, 80, 491, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.check_fullscreen = QtWidgets.QCheckBox(self.tab_3)
        self.check_fullscreen.setGeometry(QtCore.QRect(120, 50, 241, 23))
        self.check_fullscreen.setChecked(True)
        self.check_fullscreen.setObjectName("check_fullscreen")
        self.label = QtWidgets.QLabel(self.tab_3)
        self.label.setGeometry(QtCore.QRect(120, 160, 16, 17))
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(120, 190, 16, 17))
        self.label_5.setObjectName("label_5")
        self.label_8 = QtWidgets.QLabel(self.tab_3)
        self.label_8.setGeometry(QtCore.QRect(280, 160, 71, 21))
        self.label_8.setObjectName("label_8")
        self.cbox_size = QtWidgets.QComboBox(self.tab_3)
        self.cbox_size.setGeometry(QtCore.QRect(360, 160, 101, 25))
        self.cbox_size.setEditable(False)
        self.cbox_size.setObjectName("cbox_size")
        self.pushButton = QtWidgets.QPushButton(self.tab_3)
        self.pushButton.setGeometry(QtCore.QRect(140, 230, 89, 25))
        self.pushButton.setObjectName("pushButton")
        self.check_visualizar = QtWidgets.QCheckBox(self.tab_3)
        self.check_visualizar.setGeometry(QtCore.QRect(120, 20, 161, 23))
        self.check_visualizar.setChecked(True)
        self.check_visualizar.setObjectName("check_visualizar")
        self.le_wx = QtWidgets.QSpinBox(self.tab_3)
        self.le_wx.setGeometry(QtCore.QRect(140, 160, 111, 26))
        self.le_wx.setMinimum(0)
        self.le_wx.setMaximum(1920)
        self.le_wx.setObjectName("le_wx")
        self.le_wy = QtWidgets.QSpinBox(self.tab_3)
        self.le_wy.setGeometry(QtCore.QRect(140, 190, 111, 26))
        self.le_wy.setMinimum(0)
        self.le_wy.setMaximum(1080)
        self.le_wy.setObjectName("le_wy")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(120, 130, 161, 17))
        self.label_2.setObjectName("label_2")
        self.label_18 = QtWidgets.QLabel(self.tab_3)
        self.label_18.setGeometry(QtCore.QRect(120, 100, 131, 17))
        self.label_18.setObjectName("label_18")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.lb_image = QtWidgets.QLabel(self.tab_2)
        self.lb_image.setEnabled(True)
        self.lb_image.setGeometry(QtCore.QRect(220, 30, 320, 240))
        self.lb_image.setStatusTip("")
        self.lb_image.setText("")
        self.lb_image.setTextFormat(QtCore.Qt.PlainText)
        self.lb_image.setObjectName("lb_image")
        self.label_10 = QtWidgets.QLabel(self.tab_2)
        self.label_10.setGeometry(QtCore.QRect(10, 50, 51, 20))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        self.label_11.setGeometry(QtCore.QRect(10, 90, 51, 20))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        self.label_12.setGeometry(QtCore.QRect(10, 130, 51, 17))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.tab_2)
        self.label_13.setGeometry(QtCore.QRect(20, 170, 41, 17))
        self.label_13.setObjectName("label_13")
        self.crop_x = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.crop_x.setGeometry(QtCore.QRect(70, 50, 69, 26))
        self.crop_x.setDecimals(2)
        self.crop_x.setMaximum(1.0)
        self.crop_x.setSingleStep(0.1)
        self.crop_x.setObjectName("crop_x")
        self.crop_y = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.crop_y.setGeometry(QtCore.QRect(70, 90, 69, 26))
        self.crop_y.setDecimals(2)
        self.crop_y.setMaximum(1.0)
        self.crop_y.setSingleStep(0.1)
        self.crop_y.setObjectName("crop_y")
        self.crop_width = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.crop_width.setGeometry(QtCore.QRect(70, 130, 69, 26))
        self.crop_width.setDecimals(2)
        self.crop_width.setMaximum(1.0)
        self.crop_width.setSingleStep(0.1)
        self.crop_width.setProperty("value", 1.0)
        self.crop_width.setObjectName("crop_width")
        self.crop_height = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.crop_height.setGeometry(QtCore.QRect(70, 170, 69, 26))
        self.crop_height.setDecimals(2)
        self.crop_height.setMaximum(1.0)
        self.crop_height.setSingleStep(0.1)
        self.crop_height.setProperty("value", 1.0)
        self.crop_height.setObjectName("crop_height")
        self.button_preview = QtWidgets.QPushButton(self.tab_2)
        self.button_preview.setGeometry(QtCore.QRect(40, 210, 89, 25))
        self.button_preview.setObjectName("button_preview")
        self.line_2 = QtWidgets.QFrame(self.tab_2)
        self.line_2.setGeometry(QtCore.QRect(163, 30, 20, 241))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_15 = QtWidgets.QLabel(self.tab_2)
        self.label_15.setGeometry(QtCore.QRect(220, 10, 361, 20))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.tab_2)
        self.label_16.setGeometry(QtCore.QRect(200, 20, 21, 251))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.tab_2)
        self.label_17.setGeometry(QtCore.QRect(20, 10, 131, 17))
        self.label_17.setObjectName("label_17")
        self.tabWidget.addTab(self.tab_2, "")
        #------------------------------------------------------
        # AGREGADO DE RESOLUCION Y RESIZE
        #------------------------------------------------------

        self.cbox_size.addItem("1")
        self.cbox_size.addItem("2")
        self.cbox_size.addItem("3")
        #self.qbox_resolucion.addItem("default")
        self.qbox_resolucion.addItem("1920x1080")
        self.qbox_resolucion.addItem("1640x1232")
        self.qbox_resolucion.addItem("1280x720")
        self.qbox_resolucion.addItem("640x480")
        
        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.qbox_resolucion.setCurrentIndex(-1)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.cargar_configs()
        
    #-----------------------------
    #   INICIO DE FUNCIONES
    #-----------------------------
        self.button_preview.clicked.connect(self.preview_image)
        self.crop_x.valueChanged.connect(self.mantener_cuadroX)
        self.crop_y.valueChanged.connect(self.mantener_cuadroY)
        self.crop_width.valueChanged.connect(self.mantener_cuadroX)
        self.crop_height.valueChanged.connect(self.mantener_cuadroY)
        self.check_visualizar.toggled.connect(self.visualizar_change)
        self.check_fullscreen.toggled.connect(self.fullscreen_change)

        self.btn_tiempo_default.released.connect(self.tiempo_default)
        
        self.pushButton.clicked.connect(self.preview_video)
        self.le_fecha.dateTimeChanged.connect(self.update_time)
        self.le_hora.dateTimeChanged.connect(self.update_time)
        
        self.buttonBox.accepted.connect(self.guardar_configs)

    def tiempo_default(self):
        self.le_cantidad.setValue(12)
        self.le_duracion.setTime(QTime(0,30,0))
        self.le_iniciofecha.setDate(QDate.currentDate())
        now = QTime.currentTime()
        self.le_inicio.setTime(QTime(now.hour(),now.minute()+1))

    def update_time(self):
        string_time1 = self.le_fecha.date().toPyDate().strftime('%y-%m-%d')
        print (string_time1)
        string_time2=self.le_hora.time().toString()
        #string_time2 = self.dateEdit.date().toPyDate().strftime('%m/%d/%y')
        print (string_time2)
        #date_chain = "\"" + string_time1 + " " + string_time2 + "\""
        date_chain = "'20" + string_time1 + " " + string_time2 + "'"
        command = "sudo date --set "
    #command = "sudo hwclock --set --date="
        os.system (command + date_chain)
        print(command + date_chain)

    def preview_video(self):
        camera=PiCamera()
        res_x, res_y = map(int, self.qbox_resolucion.currentText().split('x'))
        camera.resolution = (res_x, res_y)
        wx=self.le_wx.value()
        wy=self.le_wy.value()
        resize=int(self.cbox_size.currentText())
        camera.start_preview(fullscreen=False, window=(wx,wy,int(640/resize),int(480/resize)))
        sleep(3)
        camera.stop_preview()
        camera.close()

    def cargar_configs(self):
        self.configs = load_configs(DEFAULT_CONFIGS_PATH)
        tiempo = self.configs['tiempo']
        fh_inicio: dt.datetime = tiempo['fh_inicio']
        self.le_inicio.setTime(QTime(fh_inicio.hour,fh_inicio.minute))
        self.le_iniciofecha.setDate(QDate(fh_inicio.year,fh_inicio.month,fh_inicio.day))
        duracion: dt.time = tiempo['duracion_videos']
        self.le_duracion.setTime(QTime(duracion.hour,duracion.minute,duracion.second))
        self.le_cantidad.setValue(tiempo['cantidad_videos'])

        grabacion = self.configs['grabacion']
        res_x, res_y = grabacion['res_x'], grabacion['res_y']
        res_idx = self.qbox_resolucion.findText(f"{res_x}x{res_y}")
        self.qbox_resolucion.setCurrentIndex(res_idx)
        self.checkBox_convertir.setChecked(grabacion['convert_mp4'])

        preview = self.configs['preview']
        self.check_visualizar.setChecked(preview['on'])
        self.check_fullscreen.setChecked(preview['fullscreen'])
        self.le_wx.setValue(preview['pos_x'])
        self.le_wy.setValue(preview['pos_y'])
        scale_idx = self.cbox_size.findText(str(preview['scale']))
        self.cbox_size.setCurrentIndex(scale_idx)

        # TODO: cargar tabla [crop]
    
    def guardar_configs(self):
        tiempo = self.configs['tiempo']
        fecha_inicio = self.le_iniciofecha.date()
        hora_inicio = self.le_inicio.time()
        tiempo['fh_inicio'] = dt.datetime(
            year=fecha_inicio.year(),
            month=fecha_inicio.month(),
            day=fecha_inicio.day(),
            hour=hora_inicio.hour(),
            minute=hora_inicio.minute(),
        )
        tiempo['duracion_videos'] = dt.time(
            hour=self.le_duracion.time().hour(),
            minute=self.le_duracion.time().minute(),
            second=self.le_duracion.time().second(),
        )
        tiempo['cantidad_videos'] = self.le_cantidad.value()

        grabacion = self.configs['grabacion']
        res_x, res_y = map(int, self.qbox_resolucion.currentText().split('x'))
        grabacion['res_x'] = res_x
        grabacion['res_y'] = res_y
        grabacion['convert_mp4'] = self.checkBox_convertir.isChecked()

        preview = self.configs['preview']
        preview['on'] = self.check_visualizar.isChecked()
        preview['fullscreen'] = self.check_fullscreen.isChecked()
        preview['pos_x'] = self.le_wx.value()
        preview['pos_y'] = self.le_wy.value()
        preview['scale'] = int(self.cbox_size.currentText())

        # TODO: editar tabla [crop]

        save_configs(self.configs, DEFAULT_CONFIGS_PATH)

    def visualizar_change(self):
        if (self.check_visualizar.isChecked()):
            self.check_fullscreen.setEnabled(True)
            self.le_wx.setEnabled(True)
            self.le_wy.setEnabled(True)
            self.cbox_size.setEnabled(False)
        else:
            self.check_fullscreen.setEnabled(False)
            self.le_wx.setEnabled(False)
            self.le_wy.setEnabled(False)
            self.cbox_size.setEnabled(False)

    def fullscreen_change(self):
        if (self.check_fullscreen.isChecked()):
            self.le_wx.setEnabled(False)
            self.le_wy.setEnabled(False)
            self.cbox_size.setEnabled(False)
        else:
            self.le_wx.setEnabled(True)
            self.le_wy.setEnabled(True)
            self.cbox_size.setEnabled(True)
    

    ##############################
    #FALTA IMPLEMENTAR ESTE CODIGO 
    ##############################
    #-----------------------------
    #   PESTANIA de Crop
    #   Mantiene el cuadrado dentro de los limites
    #-----------------------------

    def mantener_cuadroX(self):
        x=self.crop_x.value()
        w=self.crop_width.value()       
        if (x+w)>1:
            self.crop_width.setValue(1-x)
        self.crop_height.setValue(self.crop_width.value())

    def mantener_cuadroY(self):
        y=self.crop_y.value()
        h=self.crop_height.value()      
        if (y+h)>1:
            self.crop_height.setValue(1-y)      
        self.crop_width.setValue(self.crop_height.value())

    #-----------------------------
    #   PESTANIA de CROP
    #   Vista previa del crop
    #-----------------------------

    def preview_image(self):
        camera=PiCamera()
        camera.resolution = (int(self.resolucion_x),int(self.resolucion_y))
        camera.capture('/home/pi/Desktop/ant_project/image.jpg')
        #camera.stop_preview()
        camera.close()
        #camera.stop_recording()
        
        filename = "image.jpg"
        # convert image file into pixmap
        self.pixmap_image = QtGui.QPixmap(filename)

        # create painter instance with pixmap
        self.painterInstance = QtGui.QPainter(self.pixmap_image)

        # set rectangle color and thickness
        self.penRectangle = QtGui.QPen(QtCore.Qt.red)
        self.penRectangle.setWidth(3)

        lbw=self.lb_image.width()
        lbh=self.lb_image.height()
        
        # draw rectangle on painter
        k1=k2=2
        if(int(self.resolucion_x)==1920): 
            k1=6
            k2=4.5
        if(int(self.resolucion_x)==1640): 
            k1=5.12
            k2=5.13
        if(int(self.resolucion_x)==1280): 
            k1=4
            k2=3
  
        cx=self.crop_x.value()*lbw*k1
        cy=self.crop_y.value()*lbh*k2
        cw=self.crop_width.value()*lbw*k1
        ch=self.crop_height.value()*lbh*k2

        self.pixmap_image.scaled(lbw,lbh)

        self.lb_image.setScaledContents(True)
        self.painterInstance.setPen(self.penRectangle)
        self.painterInstance.drawRect(cx,cy,cw,ch)
        self.painterInstance.end()
        self.lb_image.setPixmap(self.pixmap_image)
        self.lb_image.show()
        archivo=open("crop.txt", 'w')
        archivo.write(str(self.crop_x.value())+"\n"+str(self.crop_y.value())+"\n"+str(self.crop_width.value())+"\n"+str(self.crop_height.value()))
        archivo.close()

    #-----------------------------
    #   NOMBRE DE OBJETOS
    #-----------------------------


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_9.setText(_translate("Dialog", "Fecha actual"))
        self.label_14.setText(_translate("Dialog", "Hora actual"))
        self.btn_tiempo_default.setText(_translate("Dialog", "Tiempo por defecto"))
        self.le_iniciofecha_lbl.setText(_translate("Dialog", "Inicio video (día):"))
        self.le_inicio_lbl.setText(_translate("Dialog", "Inicio video (hora):"))
        self.label_6.setText(_translate("Dialog", "Duracion:"))
        self.label_4.setText(_translate("Dialog", "Cantidad de videos:"))
        self.label_21.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#2e3436;\">*Tiempo por defecto: </span></p><p><span style=\" color:#2e3436;\">Graba video automaticamente</span></p><p><span style=\" color:#2e3436;\">Duración: 6 horas</span></p><p><span style=\" color:#2e3436;\">Tamaño de los videos: 30 minutos</span></p><p><span style=\" color:#2e3436;\">Total videos: 48</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Tiempo"))
        self.label_7.setText(_translate("Dialog", "Resolución"))
        self.checkBox_convertir.setText(_translate("Dialog", "Convertir video a *.mp4"))
        self.label_19.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#2e3436;\">(El video se graba en *.h264 por defecto)</span></p></body></html>"))
        self.label_20.setText(_translate("Dialog", "<html><head/><body><p><span style=\" color:#2e3436;\">(Se recomienda 640 x 480 si se tiene poco espacio)</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Video), _translate("Dialog", "Video"))
        self.check_fullscreen.setText(_translate("Dialog", "Fullscreen (pantalla completa)"))
        self.label.setText(_translate("Dialog", "x"))
        self.label_5.setText(_translate("Dialog", "y"))
        self.label_8.setText(_translate("Dialog", "Escalado "))
        self.pushButton.setText(_translate("Dialog", "Ver"))
        self.check_visualizar.setText(_translate("Dialog", "Visualizar"))
        self.label_2.setText(_translate("Dialog", "Posición del video"))
        self.label_18.setText(_translate("Dialog", "<html><head/><body><p><span style=\" text-decoration: underline; color:#cc0000;\">Función avanzada</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Visualizacion"))
        self.label_10.setText(_translate("Dialog", "<html><head/><body><p align=\"right\">pos. X</p></body></html>"))
        self.label_11.setText(_translate("Dialog", "<html><head/><body><p align=\"right\">pos. Y</p></body></html>"))
        self.label_12.setText(_translate("Dialog", "<html><head/><body><p align=\"right\">Ancho</p></body></html>"))
        self.label_13.setText(_translate("Dialog", "<html><head/><body><p align=\"right\">Alto</p></body></html>"))
        self.button_preview.setText(_translate("Dialog", "Ver"))
        self.label_15.setText(_translate("Dialog", "0          .          .           .        0.5        .          .          .          1.0=X"))
        self.label_16.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">0 </p><p align=\"center\">. </p><p align=\"center\">. </p><p align=\"center\">. </p><p align=\"center\">0.5 </p><p align=\"center\">. </p><p align=\"center\">. </p><p align=\"center\">. </p><p align=\"center\">1.0<br/></p></body></html>"))
        self.label_17.setText(_translate("Dialog", "<html><head/><body><p><span style=\" text-decoration: underline; color:#cc0000;\">Función avanzada</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Crop"))


class Ui_ConeccionWifi(object):
    def setupUi(self, ConeccionWifi):
        ConeccionWifi.setObjectName("ConeccionWifi")
        ConeccionWifi.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConeccionWifi)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.le_ssid = QtWidgets.QLineEdit(ConeccionWifi)
        self.le_ssid.setGeometry(QtCore.QRect(190, 40, 113, 25))
        self.le_ssid.setObjectName("le_ssid")
        self.le_pwd = QtWidgets.QLineEdit(ConeccionWifi)
        self.le_pwd.setGeometry(QtCore.QRect(190, 80, 113, 25))
        self.le_pwd.setObjectName("le_pwd")
        self.label = QtWidgets.QLabel(ConeccionWifi)
        self.label.setGeometry(QtCore.QRect(110, 40, 78, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(ConeccionWifi)
        self.label_2.setGeometry(QtCore.QRect(110, 80, 78, 17))
        self.label_2.setObjectName("label_2")
        self.pushButton_conectar = QtWidgets.QPushButton(ConeccionWifi)
        self.pushButton_conectar.setGeometry(QtCore.QRect(150, 120, 89, 25))
        self.pushButton_conectar.setObjectName("pushButton_conectar")
        self.label_3 = QtWidgets.QLabel(ConeccionWifi)
        self.label_3.setGeometry(QtCore.QRect(110, 160, 67, 17))
        self.label_3.setObjectName("label_3")
        self.lb_estadoWifi = QtWidgets.QLabel(ConeccionWifi)
        self.lb_estadoWifi.setGeometry(QtCore.QRect(180, 160, 131, 21))
        self.lb_estadoWifi.setObjectName("lb_estadoWifi")

        self.retranslateUi(ConeccionWifi)
        self.buttonBox.accepted.connect(ConeccionWifi.accept)
        self.buttonBox.rejected.connect(ConeccionWifi.reject)
        QtCore.QMetaObject.connectSlotsByName(ConeccionWifi)

        self.pushButton_conectar.clicked.connect(self.conectar_Wifi)

    def conectar_Wifi(self):
        ssid = self.le_ssid.text()
        passw = self.le_pwd.text()
        try:
            command1 = "echo 'network={' | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf"
            command2 = "echo '        ssid=\"" + ssid + "\"' | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf"
            command3 = "echo '        psk=\""  + passw + "\"' | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf"
            command4 = "echo '        key_mgmt=WPA-PSK' | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf"
            command5 = "echo '}' | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf"
            self.lb_estadoWifi.setText("Conectado")
            self.lb_estadoWifi.setStyleSheet("color: rgb(78, 154, 6);")
        except:
            self.lb_estadoWifi.setText("Desconectado")
            self.lb_estadoWifi.setStyleSheet("color: rgb(239, 41, 41);")
        self.lb_estadoWifi.setFont(QtGui.QFont("Ubuntu",weight=QtGui.QFont.Bold))

    def retranslateUi(self, ConeccionWifi):
        _translate = QtCore.QCoreApplication.translate
        ConeccionWifi.setWindowTitle(_translate("Dialog", "Configuración de Conexion"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p>SSID</p></body></html>"))
        self.label_2.setText(_translate("Dialog", "Password"))
        self.pushButton_conectar.setText(_translate("Dialog", "Conectar"))
        self.label_3.setText(_translate("Dialog", "Estado:"))
        self.lb_estadoWifi.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ef2929;\">Desconectado</span></p></body></html>"))

class ConeccionWifi(QDialog):
                                   # <===
    def __init__(self, *args, **kwargs):
        super(ConeccionWifi, self).__init__(*args, **kwargs)
        self.setWindowTitle("Configuracion de Wifi")

class ConfigurarPantalla(QDialog):
                                   # <===
    def __init__(self, *args, **kwargs):
        super(ConfigurarPantalla, self).__init__(*args, **kwargs)
        self.setWindowTitle("Configuracion de Wifi")


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(640, 308)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(39, 20, 571, 103))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
       # self.t_temperatura = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
       # self.t_temperatura.setObjectName("t_temperatura")
        #self.horizontalLayout_2.addWidget(self.t_temperatura)
       # self.lb_temperatura = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
       # self.lb_temperatura.setObjectName("lb_temperatura")
       # self.horizontalLayout_2.addWidget(self.lb_temperatura)
       # self.t_humedad = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
       # self.t_humedad.setObjectName("t_humedad")
        # self.horizontalLayout_2.addWidget(self.t_humedad)
        #self.lb_humedad = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        #self.lb_humedad.setObjectName("lb_humedad")
        #self.horizontalLayout_2.addWidget(self.lb_humedad)
       # self.t_luz = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
       # self.t_luz.setObjectName("t_luz")
       # self.horizontalLayout_2.addWidget(self.t_luz)
        #self.lb_luz = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        #self.lb_luz.setObjectName("lb_luz")
        #self.horizontalLayout_2.addWidget(self.lb_luz)
        self.status_mainBar = QtWidgets.QLabel(self.centralwidget)
        self.status_mainBar.setEnabled(True)
        self.status_mainBar.setGeometry(QtCore.QRect(170, 130, 421, 39))
        
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 225))
        brush.setStyle(QtCore.Qt.SolidPattern)    
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        self.status_mainBar.setPalette(palette)


        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.status_mainBar.setFont(font)
        self.status_mainBar.setObjectName("status_mainBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(100, 140, 67, 17))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName("menubar")
        self.menuSistema = QtWidgets.QMenu(self.menubar)
        self.menuSistema.setObjectName("menuSistema")
        self.menuBase_de_Datox = QtWidgets.QMenu(self.menubar)
        self.menuBase_de_Datox.setObjectName("menuBase_de_Datox")
        self.menuAyuda = QtWidgets.QMenu(self.menubar)
        self.menuAyuda.setObjectName("menuAyuda")
        self.menuConfiguraci_on = QtWidgets.QMenu(self.menubar)
        self.menuConfiguraci_on.setObjectName("menuConfiguraci_on")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionGrabar = QtWidgets.QAction(MainWindow)
        self.actionGrabar.setObjectName("actionGrabar")
        self.actionConexion = QtWidgets.QAction(MainWindow)
        self.actionConexion.setObjectName("actionConexion")
        self.actionConexion_configuracion = QtWidgets.QAction(MainWindow)
        self.actionConexion_configuracion.setObjectName("actionConexion_configuracion")
        self.actionRecord = QtWidgets.QAction(QIcon("play.png"), "Your button", self)
        self.actionRecord.setObjectName("actionRecord")
        self.actionStop = QtWidgets.QAction(QIcon("stop.png"), "Your button", self)
        self.actionStop.setObjectName("actionStop")
        self.actionConection = QtWidgets.QAction(QIcon("wifi.png"), "Your button", self)
        self.actionConection.setObjectName("actionConection")
        self.button_action = QAction(QIcon("bug.png"), "Your button", self)
        self.actionCargar_configuracion = QtWidgets.QAction(MainWindow)
        self.actionCargar_configuracion.setObjectName("actionCargar_configuracion")
        self.actionConsultarBD = QtWidgets.QAction(MainWindow)
        self.actionConsultarBD.setObjectName("actionConsultarBD")
        self.actionCargarBD = QtWidgets.QAction(MainWindow)
        self.actionCargarBD.setObjectName("actionCargarBD")
        self.actionGuardarBD = QtWidgets.QAction(MainWindow)
        self.actionGuardarBD.setObjectName("actionGuardarBD")
        self.actionManual = QtWidgets.QAction(MainWindow)
        self.actionManual.setObjectName("actionManual")
        self.actionAcerca_de_Ant_Project = QtWidgets.QAction(MainWindow)
        self.actionAcerca_de_Ant_Project.setObjectName("actionAcerca_de_Ant_Project")
        self.actionConfigurar = QtWidgets.QAction(QIcon("cfg.png"), "Your button", self)
        self.actionConfigurar.setObjectName("actionConfigurar")
        self.actionGuardar_configuracion = QtWidgets.QAction(MainWindow)
        self.actionGuardar_configuracion.setObjectName("actionGuardar_configuracion")
        self.actionPantalla_configuracion = QtWidgets.QAction(MainWindow)
        self.actionPantalla_configuracion.setObjectName("actionPantalla_configuracion")
        self.actionSalir = QtWidgets.QAction(MainWindow)
        self.actionSalir.setObjectName("actionSalir")
        self.actionImprimir = QtWidgets.QAction(MainWindow)
        self.actionImprimir.setObjectName("actionImprimir")
        self.menuSistema.addSeparator()
        self.menuSistema.addSeparator()
        self.menuSistema.addAction(self.actionImprimir)
        self.menuSistema.addAction(self.actionSalir)
        self.menuBase_de_Datox.addSeparator()
        self.menuBase_de_Datox.addAction(self.actionConsultarBD)
        self.menuBase_de_Datox.addSeparator()
        self.menuBase_de_Datox.addAction(self.actionCargarBD)
        self.menuBase_de_Datox.addAction(self.actionGuardarBD)
        self.menuAyuda.addSeparator()
        self.menuAyuda.addAction(self.actionManual)
        self.menuAyuda.addAction(self.actionAcerca_de_Ant_Project)
        self.menuConfiguraci_on.addSeparator()
        self.menuConfiguraci_on.addAction(self.actionConexion_configuracion)
        self.menuConfiguraci_on.addAction(self.actionPantalla_configuracion)
        self.menuConfiguraci_on.addSeparator()
        self.menuConfiguraci_on.addAction(self.actionCargar_configuracion)
        self.menuConfiguraci_on.addAction(self.actionGuardar_configuracion)
        self.menubar.addAction(self.menuSistema.menuAction())
        self.menubar.addAction(self.menuConfiguraci_on.menuAction())
        self.menubar.addAction(self.menuBase_de_Datox.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())
        self.toolBar.addAction(self.actionRecord)
        self.toolBar.addAction(self.actionStop)
        self.toolBar.addAction(self.actionConection)
        self.toolBar.addAction(self.actionConfigurar)
        #elf.toolBar.addAction(self.actionConfiguration)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        #def hilo_sensado():
         #   start=dt.datetime.now()
          #  t_record=5
           # formato="%Y%m%d"
            #formato_2="%Y%m%d-%H%M%S"
            #fecha=dt.datetime.now()
            #name='log_'+fecha.strftime(formato)+'.txt'

         #   while True:
               # s_Luz=str(format(readLight(),'.2f'))
            #    s_Humedad, s_Temperatura = Adafruit_DHT.read_retry(sensor, temp_gpio)
             #   s_Temperatura=format(s_Temperatura, '.2f')
              #  s_Humedad=format(s_Humedad, '.2f')
               # newfont = QtGui.QFont("Ubuntu", 20)
                #self.lb_temperatura.setText(str(s_Temperatura)+"°C")
                #self.lb_humedad.setText(str(s_Humedad)+"%")
               # self.lb_luz.setText(s_Luz)
                #self.lb_temperatura.setFont(newfont)
                #self.lb_humedad.setFont(newfont)
                #self.lb_luz.setFont(newfont)

               # if((dt.datetime.now() - start).seconds > t_record):
                #    try:
                 #       archivo = open(name,'a')
                  #  except:
                   #     archivo = open(name,'w')
                   # archivo.write(str(s_Temperatura)+" ")
                   # archivo.write(str(s_Humedad)+" ")
                 #   archivo.write(str(s_Luz)+" ")
                    #archivo.write((dt.datetime.now()).strftime(formato_2)+"\n")
                    #archivo.close()
                    #print('guardando sensados '+(dt.datetime.now()).strftime(formato_2))

                    #start=dt.datetime.now()

                #sleep(2)

        #hilo0 = threading.Thread(target=hilo_sensado)
        #hilo0.start()


        #----------------------------------------------------------
        #FUNCIONES DEL MENU
        #----------------------------------------------------------

        self.actionConexion_configuracion.triggered.connect(self.show_coneccion)
        self.actionConection.triggered.connect(self.show_coneccion)
        self.actionPantalla_configuracion.triggered.connect(self.show_pantalla)
        self.actionConfigurar.triggered.connect(self.show_pantalla)
        self.actionStop.triggered.connect(self.detener_grabacion)
        self.actionRecord.triggered.connect(self.grabar_video)
        self.actionGuardar_configuracion.triggered.connect(self.grabar_video)
        #self.actionConfiguration.triggered.connect(self.show_config)   
        #self.actionRecord.triggered.connect(self.grabar_video)    
        #self.retranslateUi(MainWindow)
        #QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #self.actionc_on.setText("Esperando orden...")
        self.actionSalir.triggered.connect(self.salir)

    def salir(self):
            QCoreApplication.quit()

    def detener_grabacion(self):
            camera.stop_preview()
            camera.stop_recording()
            camera.close()

    def grabar_video(self):
        def hilo_grabar_video():
            newfont = QtGui.QFont("Ubuntu", 36) 
            self.status_mainBar.setText("Grabando video")
            #self.lb_temperatura.setFont(newfont)
            try:
                p=subprocess.Popen(args=["python3", "video.py"])
                p.wait()
            except:
                print("CANCELADO")
            self.status_mainBar.setText("Esperando una accion")
           # self.lb_temperatura.setFont(newfont)


                

        hilo1 = threading.Thread(target=hilo_grabar_video)

        hilo1.start()




    def show_pantalla(self):
        dialog = ConfigurarPantalla(self)  # self hace referencia al padre
        dialog.ui=Ui_ConfigurarPantalla()
        dialog.ui.setupUi(dialog)
        dialog.show()        

    def show_coneccion(self):                                            
        dialog = ConeccionWifi(self)  # self hace referencia al padre
        dialog.ui=Ui_ConeccionWifi()
        dialog.ui.setupUi(dialog)
        dialog.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ANTVRecord"))
        #self.t_temperatura.setText(_translate("MainWindow", "Temperatura:"))
        #self.lb_temperatura.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:36pt;\">0°</span></p></body></html>"))
        #self.t_humedad.setText(_translate("MainWindow", "Humedad:"))
        #self.lb_humedad.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:36pt;\">0</span></p></body></html>"))
       # self.t_luz.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Luz:</p></body></html>"))
       # self.lb_luz.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:36pt;\">0</span></p></body></html>"))
        self.status_mainBar.setText(_translate("MainWindow", "<html><head/><body><p>Esperando una accion</p></body></html>"))
        self.label.setText(_translate("MainWindow", "Estado:"))
        self.menuSistema.setTitle(_translate("MainWindow", "Sistema"))
        self.menuBase_de_Datox.setTitle(_translate("MainWindow", "Base de Datos"))
        self.menuAyuda.setTitle(_translate("MainWindow", "Ayuda"))
        self.menuConfiguraci_on.setTitle(_translate("MainWindow", "Configuracion"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionGrabar.setText(_translate("MainWindow", "Grabar"))
        self.actionConexion.setText(_translate("MainWindow", "Conexion"))
        self.actionConexion_configuracion.setText(_translate("MainWindow", "Conectar"))
        self.actionRecord.setText(_translate("MainWindow", "Grabar"))
        self.actionStop.setText(_translate("MainWindow", "Parar"))
        self.actionStop.setEnabled(True)
        self.actionConection.setText(_translate("MainWindow", "Conectar"))
        self.actionCargar_configuracion.setText(_translate("MainWindow", "Cargar configuracion"))
        self.actionConsultarBD.setText(_translate("MainWindow", "Consultar"))
        self.actionCargarBD.setText(_translate("MainWindow", "Cargar"))
        self.actionGuardarBD.setText(_translate("MainWindow", "Guardar"))
        self.actionManual.setText(_translate("MainWindow", "Manual"))
        self.actionAcerca_de_Ant_Project.setText(_translate("MainWindow", "Acerca de Ant Project"))
        self.actionConfigurar.setText(_translate("MainWindow", "Configurar"))
        self.actionGuardar_configuracion.setText(_translate("MainWindow", "Guardar configuracion"))
        self.actionPantalla_configuracion.setText(_translate("MainWindow", "Configurar pantalla"))
        self.actionSalir.setText(_translate("MainWindow", "Salir"))
        self.actionImprimir.setText(_translate("MainWindow", "Imprimir"))



if __name__ == "__main__":
    import sys
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
