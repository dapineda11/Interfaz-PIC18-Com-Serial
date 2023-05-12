'''
Pontificia Universidad Javeriana
Proyecto 2
Interfaz Gráfica de usuario
'''

from tkinter import *
import serial.tools.list_ports
import serial
import threading
import signal
import sys
import numpy as np



def MantenerGrafico(signum, frame):
    sys.exit()

signal.signal(signal.SIGINT, MantenerGrafico)

class Graphics():
    pass

class Graphics2():
    pass

class Graphics3():
    pass

def Menu_Usuario():
    '''Creacion objeto ventana'''
    global VentanaInterfaz,BotonConectar,BotonRefrescar, BotonEnviar ,BarraComandos,TacoCorriente, RegistroHist
    VentanaInterfaz = Tk()

    #Tamaño
    VentanaInterfaz.geometry('1280x720')
    VentanaInterfaz.config(bg='grey')
#Titulos de etiqueta
    VentanaInterfaz.title("Interfaz de usuario, monitoreo de batería")
    nota = Label(VentanaInterfaz, text='INTERFAZ GRÁFICA DE RECEPCIÓN Y TRANSMISIÓN SERIAL', bg='dark grey')
    nota.grid(column=3,row=1)
    titulo1 = Label(VentanaInterfaz, text='Pontificia Universidad Javeriana', bg='dark grey')
    titulo1.grid(column=3,row=2)

    titulo2 = Label(VentanaInterfaz, text='Grupo 2-2', bg='dark grey')
    titulo2.grid(column=3,row=3)

    EtiquetaPuertos = Label(VentanaInterfaz, text="Puertos disponibles: ", bg="dark grey")
    EtiquetaPuertos.grid(column=1, row=6, pady=20, padx=10)

    EtiquetaBaudios = Label(VentanaInterfaz, text="Tasa de Baudaje: ", bg="dark grey")
    EtiquetaBaudios.grid(column=1, row=4, pady=20, padx=10)

    #Botones de interfaz
    BotonRefrescar = Button(VentanaInterfaz, text="Actualizar COM", height=1,width=12, command=ActualizarCOMS)
    BotonRefrescar.grid(column=1, row=8)

    BotonConectar = Button(VentanaInterfaz, text="Conectar", height=2,width=10, state="disabled", command=ControlConexion)
    BotonConectar.grid(column=2, row=6)

    BotonEnviar= Button(VentanaInterfaz, text="Enviar",height=1, command=Comandos)
    BotonEnviar.grid(column=5, row=5)

    ComandoIngresado=0
    BarraComandos = Entry(VentanaInterfaz, width=40, bg='black',highlightcolor='white',selectforeground='white',selectbackground='green',fg='green',textvariable=ComandoIngresado)
    BarraComandos.grid(column=4, row=5)

    EtiquetaPuertos = Label(VentanaInterfaz, text="Ingresar comando:", bg="dark grey")
    EtiquetaPuertos.grid(column=4, row=4, pady=20, padx=10)

    RegistroHist=Text(VentanaInterfaz, width=30, height=3)
    RegistroHist.grid(column=4, row=8)

    EtiquetaRegH = Label(VentanaInterfaz, text="Registro de históricos:", bg="dark grey")
    EtiquetaRegH.grid(column=4, row=7, pady=20, padx=10)

    SeleccionarBaudios()
    ActualizarCOMS()

#Tacometro Corriente
    TacoCorriente=Graphics()

    EtiquetaC = Label(VentanaInterfaz, text="Corriente", bg="dark grey")
    EtiquetaC.grid(column=1, row=11, pady=20, padx=10)

    TacoCorriente.canvas= Canvas(VentanaInterfaz, width=200, height=200, bg='white', highlightthickness=1)
    TacoCorriente.canvas.grid(column=1, row=10)

    TacoCorriente.outer = TacoCorriente.canvas.create_arc(10, 10, 190, 190, start=90, extent=40, outline="#093e07", fill="#09ff00", width=5)
    # Static
    TacoCorriente.canvas.create_oval(65, 65, 140, 140, outline="#093e07", fill="#09ff00", width=5)
    # Dynamic update
    TacoCorriente.text = TacoCorriente.canvas.create_text(90, 100, font=("Times", "18"), text="---")
    # Static
    TacoCorriente.canvas.create_text(115, 100, anchor=CENTER, font=("Times", "18"), text=" A")

#Tacometro Voltaje
    TacoVoltaje=Graphics2()

    EtiquetaV = Label(VentanaInterfaz, text="Voltaje", bg="dark grey")
    EtiquetaV.grid(column=2, row=11, pady=20, padx=10)

    TacoVoltaje.canvas= Canvas(VentanaInterfaz, width=200, height=200, bg='white', highlightthickness=1)
    TacoVoltaje.canvas.grid(column=2, row=10)

    TacoVoltaje.outer = TacoVoltaje.canvas.create_arc(10, 10, 190, 190, start=90, extent=40, outline="#370d67", fill="#8e5cc6", width=5)
    # Static
    TacoVoltaje.canvas.create_oval(65, 65, 140, 140, outline="#370d67", fill="#8e5cc6", width=5)

    TacoVoltaje.text = TacoVoltaje.canvas.create_text(90, 100, font=("Times", "20"), text="---")

    TacoVoltaje.canvas.create_text(115, 100, anchor=CENTER, font=("Times", "25"), text="V")

#Tacometro Temperatura
    TacoTemperatura=Graphics3()


    EtiquetaT = Label(VentanaInterfaz, text="Temperatura", bg="dark grey")
    EtiquetaT.grid(column=3, row=11, pady=20, padx=10)

    TacoTemperatura.canvas= Canvas(VentanaInterfaz, width=200, height=200, bg='white', highlightthickness=1)
    TacoTemperatura.canvas.grid(column=3, row=10)

    TacoTemperatura.outer = TacoTemperatura.canvas.create_arc(10, 10, 190, 190, start=90, extent=40, outline="#070e3e", fill="#00ffe4", width=5)

    TacoTemperatura.canvas.create_oval(65, 65, 140, 140, outline="#070e3e", fill="#00ffe4", width=5)

    TacoTemperatura.text = TacoTemperatura.canvas.create_text(90, 100, font=("Times", "15"), text="---")

    TacoTemperatura.canvas.create_text(115, 100, anchor=CENTER, font=("Times", "20"), text="°C")

def RevisarConexion(args):
    if "-" in COMSeleccionado.get() or "-" in BaudajeSeleccionado.get():
        BotonConectar["state"] = "disable"
    else:
        BotonConectar["state"] = "active"

def SeleccionarBaudios():
    global BaudajeSeleccionado, DesplegarBaudaje
    BaudajeSeleccionado = StringVar()
    baudiosxd = ["-", "9600","14400","19200","57600","115200","128000","256000"]
    BaudajeSeleccionado.set(baudiosxd[0])
    DesplegarBaudaje = OptionMenu(VentanaInterfaz, BaudajeSeleccionado, *baudiosxd, command=RevisarConexion)
    DesplegarBaudaje.config(width=30)
    DesplegarBaudaje.grid(column=1, row=5, padx=50)


def ActualizarCOMS():
    global COMSeleccionado, DesplegarCOMs
    PuertoPIC18 = serial.tools.list_ports.comports()
    coms = [com[0] for com in PuertoPIC18]
    coms.insert(0, "-")
    try:
        DesplegarCOMs.destroy()
    except:
        pass
    COMSeleccionado = StringVar()
    COMSeleccionado.set(coms[0])
    DesplegarCOMs = OptionMenu(VentanaInterfaz, COMSeleccionado, *coms, command=RevisarConexion)
    DesplegarCOMs.config(width=30)
    DesplegarCOMs.grid(column=1, row=7, padx=50)

    RevisarConexion(0)


def ControlParametroC(TacoCorriente):
    TacoCorriente.canvas.itemconfig(TacoCorriente.outer, exten=(TacoCorriente.sensorC))
    TacoCorriente.canvas.itemconfig(TacoCorriente.text, text=f"{(TacoCorriente.sensorC)}")

def ControlParametroV(TacoVoltaje):
    TacoVoltaje.canvas.itemconfig(TacoVoltaje.outer, exten=(TacoVoltaje.sensorV))
    TacoVoltaje.canvas.itemconfig(TacoVoltaje.text, text=f"{(TacoVoltaje.sensorV)}")

def ControlParametroT(TacoTemperatura):
    TacoTemperatura.canvas.itemconfig(TacoTemperatura.outer, exten=(TacoTemperatura.sensorT))
    TacoTemperatura.canvas.itemconfig(TacoTemperatura.text, text=f"{(TacoTemperatura.sensorT)}")




def LecturaDatosSerialesC():
    global DatoSerialC, TacoCorriente,TacoVoltaje,TacoTemperatura
    datoC, datoC1,datoC2,datoC3,datoC4, datoV, datoV1, datoV2, datoV3, datoV4, datoT,datoT1 = 0,0,0,0,0,0,0,0,0,0,0,0
    averageC,averageV,averageT = 0,0,0
    dato_sensorC,dato_sensorV,dato_sensorT=0,0,0
    sensorC,SensorV,SensorT=0,0,0
    sampling = 20
    sample = 0
    trama=[0,0,0,0,0,0,0,0,0,0]

    i = 0

    while DatoSerialC:
        if chr(int.from_bytes(ser.read(1),'little'))=='#':

            for i in range(9):
                trama[i] = ser.read(1)

            datoC1= (chr(int.from_bytes(trama[0],'little')))
            datoC2= (chr(int.from_bytes(trama[1],'little')))
            datoC3 = (chr(int.from_bytes(trama[2],'little')))
            datoC4 = (chr(int.from_bytes(trama[3], 'little')))

            #print(datoC1, datoC2, datoC3, "\n")
            if datoC1!=chr(0) and datoC2!=chr(0) and datoC3!=chr(0) and datoC4!=chr(0):
                datoC=(float(datoC1+datoC2+datoC3+datoC4))

            datoV1 = (chr(int.from_bytes(trama[4], 'little')))
            datoV2 = (chr(int.from_bytes(trama[5], 'little')))
            datoV3 = (chr(int.from_bytes(trama[6], 'little')))
            datoV4 = (chr(int.from_bytes(trama[7], 'little')))

            if datoV1!=chr(0) and datoV2!=chr(0) and datoV3!=chr(0) and datoV4!=chr(0):
                datoV=(float(datoV1+datoV2+datoV3+datoV4))

            datoT1 = (str(chr(int.from_bytes(trama[8], 'little'))))

            if datoT1!=chr(0):
                datoT=(float(datoT1))

            #datoC= (int.from_bytes(trama[0],'little')<<16)+(int.from_bytes(trama[1], 'little')<<8)+(int.from_bytes(trama[2], 'little'))
            #datoV = (int.from_bytes(trama[3], 'little') << 8) | int.from_bytes(trama[4], 'little')
            #datoT = (int.from_bytes(trama[5], 'little') << 8) | int.from_bytes(trama[6], 'little')

            #print(dato)
            try:

                data_sensorC=datoC
                averageC += data_sensorC
                data_sensorV = datoV

                averageV += data_sensorV
                data_sensorT= datoT
                averageT += data_sensorT
                sample += 1
                if sample == sampling:
                    print("Voltaje=",datoC,"\t","Temperatura=",datoV,"\t","Alerta=",datoT,"\n")
                    sensorC = np.round(averageC / sampling,1)
                    averageC = 0

                    sensorV = np.round(averageV / sampling,1)
                    averageV = 0

                    sensorT = np.round(averageT / sampling,1)
                    averageT = 0
                    sample = 0
                    # print(sensor)
                    TacoCorriente.sensorC = sensorC
                    t = threading.Thread(target=ControlParametroC, args=(TacoCorriente,))
                    t.deamon = True
                    t.start()

                    TacoVoltaje.sensorV = sensorV
                    t = threading.Thread(target=ControlParametroV, args=(TacoVoltaje,))
                    t.deamon = True
                    t.start()

                    #TacoTemperatura.sensorT = sensorT
                    #t = threading.Thread(target=ControlParametroT, args=(TacoTemperatura,))
                    #t.deamon = True
                    #t.start()


            except:
                pass
        else:
            continue

def ControlConexion():
    global ser, DatoSerialC
    if BotonConectar["text"] in "Desconectado":
        DatoSerialC = False
        BotonConectar["text"] = "Conectado"
        BotonRefrescar["state"] = "active"
        DesplegarBaudaje["state"] = "active"
        DesplegarCOMs["state"] = "active"

    else:
        DatoSerialC = True
        BotonConectar["text"] = "Conectado"
        BotonConectar["state"] = "disabled"
        BotonRefrescar["state"] = "disable"
        DesplegarBaudaje["state"] = "disable"
        DesplegarCOMs["state"] = "disable"
        port = COMSeleccionado.get()
        baud = BaudajeSeleccionado.get()
        try:
            ser = serial.Serial(port, baud, timeout=0)
        except:
            pass
        t1 = threading.Thread(target=LecturaDatosSerialesC)
        t1.deamon = True
        t1.start()

def Comandos():
    global ComandoIngresado1, VentanaInterfaz, ser, BarraComandos
    ComandoIngresado1=BarraComandos.get()
    b = ComandoIngresado1.encode()
    ser.write(b)
    #print(ComandoIngresado1)
    #print(str("\n",b))


def CerrarVentana():
    global VentanaInterfaz, DatoSerialC
    DatoSerialC = False
    VentanaInterfaz.destroy()


Menu_Usuario()
VentanaInterfaz.protocol("Cerrar Ventana", CerrarVentana)
VentanaInterfaz.mainloop()