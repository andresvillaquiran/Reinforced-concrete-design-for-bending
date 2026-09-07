# librerias ## AGREGAR ANCHO DE VIGA Y calibre y distancia cortante
import tkinter as tk 
import numpy as np # import array, roots,around, zeros
#from sympy import symbols, solve    
from math import sqrt, floor, ceil

# creamos ventana principal

def mostrar_frame(frame):
    frame.tkraise() ## trae al frame que sea llamado


# Base datos refuerzo col1 = tipo de acero, col 2 = diametro [mm], col 3 = area[m]
lista_refuerzo = np.array([[0,0,0],
                        [1,0,0],
                        [2,6.4,32],
                        [3,9.5,71],
                        [4,12.7,129],
                        [5,15.9,199],
                        [6,19.1,284],
                        [7,22.2,387],
                        [8,25.4,510],
                        [9,28.7,645],
                        [10,32.3,819],
                        [11,35.8,1006],
                        [12,38.1,1134],
                        [13,41.3,1335],
                        [14,43,1452],
                        [18,57.3,2581]])


def Analisis_viga(fc,fy,b,h,r,Vu,bv,calibre,dv):
    # Coefieciente de reduccion de cortante phi = 0.75 
    phi = 0.75

    d = h - r - 0.01 # Altura efectiva

    print(f"fc = {round(fc,3)} [MPa]")
    print(f"fy = {round(fy,3)} [MPa]")
    print(f"b = {round(b,3)} [m]")
    print(f"h = {round(h,3)} [m]")
    print(f"r = {round(r,3)} [m]")
    print(f"Vu = {round(Vu,3)} [kN*m]")
    print(f"bv = {round(bv,3)} [m]")
    print(f"calibre = {round(calibre,3)}")
    print(f"dv = {round(dv,3)} [m]")


    Av = lista_refuerzo[calibre,2]/10000

    #Resistencia cortante concreto
    Vc = phi*0.17*sqrt(fc/1000)*b*d*1000 #[kN]
    print(f"Vc = {round(Vc,3)} [kN]")
    #Maxima resistencia del refuerzo a cortante
    Vsmax = phi*0.66*sqrt(fc/1000)*b*d*1000 #[kN]
    print(f"Vsmax = {round(Vsmax,3)} [kN]")

    if Vu == 0:
        Vsreq = 0.0
        smaxd = 0
        Xvc = 0
        xmin = 0
        num_est_vc = 0
        num_est_min = 0
        long_princ = 0
    else:

        Vsreq = Vu - Vc # Cuando Vs necesito en mi viga?
        if Vsreq < 0: # Si no necesita simplemente lo hago 0
            Vsreq = 0.0


        if Vsreq< phi*0.33*sqrt(fc/1000)*b*d*1000: # El vs req supera el humbral para el smax?
            smax = min([d/2,0.6,1200*Av*b])
        else:
            smax = min([d/4,0.3,600*Av*b])

        smax_inicial = floor(smax/0.05)*0.05 # separacion de diseño en multiplo de 5cm 

        #Verifico la separacion maximo por resistencia
        if Vsreq == 0.0:
            smaxS = smax_inicial
        else:

            smaxS = phi*Av*fy*d/Vsreq # separacion maximo por resistencia
        print(f'Vsreq = {round(Vsreq,3)} [kN]')
        print(f'smaxS = {round(smaxS,3)} [m]')

        smaxS = floor(smaxS/0.05)*0.05 # separacion de diseño en multiplo de 5cm 

        smaxd = min(smax_inicial,smaxS) # separacion de diseño final 

        #Distancia de cortante DISEÑO ESTRIBOS
        #dv = 1.8 #[m] ###########
        Xvc = dv*(1-Vc/Vu) # Distancia de refuero por cortante diseñado

        if Xvc-bv/2-0.05 < bv/2+0.05:
            #Xvc = 0
            num_est_vc = 0
            long_princ = 0
            print(f'Xvc = {round(Xvc,2)} [m]')
            xmin  =  dv*(1-Vc/(2*Vu)) - bv/2-0.05
            num_est_min = ceil((xmin)/smaxd) +1  # Numero de estribos minimos

        else:
            long_princ = Xvc-bv/2-0.05
            print(f'longitud_estribos principales: ', long_princ)
            num_est_vc = ceil((long_princ)/smaxd) +1 # Numero de estribos necesarios en zona de requerimiento
            print((Xvc-bv/2-0.05)/smaxd)
            xmin = dv*(1-Vc/(2*Vu)) - Xvc # Distancia de refuerzo minimo por cortante
            num_est_min =ceil((xmin)/smaxd) # Numero de estribos minimos


        if h < 0.25:
            xmin = 0
            num_est_min = 0

        elif xmin <0:
            xmin=0
            num_est_min = 0
        else:
            num_est_min = num_est_min
            
    print(f"# estribo min = {num_est_min} ")
    print('    ')

    return smaxd, Xvc,xmin, num_est_vc, num_est_min, Vsmax, Vc, Vsreq,long_princ

ventana1 = tk.Tk()
ventana1.geometry("1200x500") ## tamaño de la ventana general
ventana1.title("Diseño viguetas Cortante ") ## titulo de la ventana general

# Creamos los frames para organizar la información

frame1 = tk.Frame(ventana1)
frame2 = tk.Frame(ventana1)

for frame in (frame1,frame2):  ## posicionamos los frames en el mismo lugar
    frame.grid(row=0, column=0, sticky='nsew')

gnum_tramos = 0
gAsmax      = 0.0
As_min       = 0.0
gAsb        = 0.0
##################################### CONTENIDO FRAME 1 #################################
#####################################                   #################################



etiq_inicio = tk.Label(frame1, text='Bienvenido a la sufridera DCR1 -- Diseñado por Andres Villaquirán ')
etiq_inicio.grid(row=0, column=0, columnspan=3, padx=5, pady=3)


etiq_ing_valores = tk.Label(frame1, text='Ingreso de parametro de la viga')
etiq_raviso = tk.Label(frame1, text='Si no conoce b de viga maestra se recomienda 0.3 m')
etiq_ing_valores.grid(row=1, column=0, padx=5, pady=3)
etiq_raviso.grid(row=1, column=1, columnspan=2 , padx=5, pady=3) # Ubicación en la cuadrícula
#etiq_ing_valores.pack(pady=1)

etiq_fc = tk.Label(frame1, text='fc [MPa]')
entrada_fc = tk.Entry(frame1)
etiq_fc.grid(row=2, column=0, padx=5, pady=3) # Ubicación en la cuadrícula
entrada_fc.grid(row=2, column=2, padx=3, pady=3) # Ubicación en la cuadrícula

etiq_fy = tk.Label(frame1, text='fy [MPa]')
entrada_fy = tk.Entry(frame1)
etiq_fy.grid(row=3, column=0, padx=5, pady=3) # Ubicación en la cuadrícula
entrada_fy.grid(row=3, column=2, padx=3, pady=3) # Ubicación en la cuadrícula

etiq_b = tk.Label(frame1, text='b [m]')
entrada_b  = tk.Entry(frame1)
etiq_b.grid(row=4, column=0, padx=10, pady=3) # Ubicación en la cuadrícula
entrada_b.grid(row=4, column=2, padx=3, pady=3) # Ubicación en la cuadrícula

etiq_bv = tk.Label(frame1, text='Ancho viga maestra [m]')
entrada_bv  = tk.Entry(frame1)
etiq_bv.grid(row=5, column=0, padx=10, pady=3) # Ubicación en la cuadrícula
entrada_bv.grid(row=5, column=2, padx=3, pady=3) # Ubicación en la cuadrícula


etiq_h = tk.Label(frame1, text='h [m]')
entrada_h  = tk.Entry(frame1)
etiq_h.grid(row=6, column=0, padx=5, pady=3) # Ubicación en la cuadrícula
entrada_h.grid(row=6, column=2, padx=3, pady=3) # Ubicación en la cuadrícula


etiq_r = tk.Label(frame1, text='r [m]')
entrada_r  = tk.Entry(frame1)
etiq_r.grid(row=7, column=0, padx=10, pady=3) # Ubicación en la cuadrícula
entrada_r.grid(row=7, column=2, padx=3, pady=3) # Ubicación en la cuadrícula

etiq_calibre = tk.Label(frame1, text='Calibre estribo ')
entrada_calibre  = tk.Entry(frame1)
etiq_calibre.grid(row=8, column=0, padx=10, pady=3) # Ubicación en la cuadrícula
entrada_calibre.grid(row=8, column=2, padx=3, pady=3) # Ubicación en la cuadrícula

'''
etiq_dv = tk.Label(frame1, text='Longitud de cortante [m]')
etiq_dv.grid(row=9, column =0, padx=5, pady=3) # Ubicación en la cuadrícula
entrada_dv = tk.Entry(frame1)
entrada_dv.grid(row=9, column =2, padx=5, pady=3)
'''

etiq_num_viguetas = tk.Label(frame1, text='Numero de tramos')
etiq_num_viguetas.grid(row=9, column =0, padx=5, pady=3) # Ubicación en la cuadrícula
entrada_num_viguetas = tk.Entry(frame1)
entrada_num_viguetas.grid(row=9, column =2, padx=5, pady=3)


## ventanas de resultados

etiq_d = tk.Label(frame1,text='d [m]')
etiq_d.grid(row=12, column=0, padx=5, pady=3) # Ubicación en la cuadrícula

etiq_Vc = tk.Label(frame1,text='Vc [kN]')
etiq_Vc.grid(row=13, column=0, padx=5, pady=3) # Ubicación en la cuadrícula

etiq_Vsmax = tk.Label(frame1,text='Vs max [kN]')
etiq_Vsmax.grid(row=14, column=0, padx=5, pady=3) # Ubicación en la cuadrícula

'''
etiq_smaxd = tk.Label(frame1,text='Separacion max [m]')
etiq_smaxd.grid(row=15, column=0, padx=5, pady=3) # Ubicación en la cuadrícula
'''


## Etiqueta de resultados


result_d = tk.Label(frame1)
result_d.grid(row=12, column=2, padx=5, pady=3) # 

result_Vc = tk.Label(frame1)
result_Vc.grid(row=13, column=2, padx=5, pady=3) # 

result_Vsmax= tk.Label(frame1)
result_Vsmax.grid(row=14, column=2, padx=5, pady=3) # 

'''
result_smaxd= tk.Label(frame1)
result_smaxd.grid(row=15, column=2, padx=5, pady=3) # 
'''

def calculo_aceros():   # Leemos las variables que entraron al principio

    fc = float(entrada_fc.get())*1000 # Convertimos a KPa
    fy = float(entrada_fy.get())*1000 # Convertimos a KPa
    b = float(entrada_b.get())
    h = float(entrada_h.get())
    r = float(entrada_r.get())
    bv = float(entrada_bv.get())
    calibre = int(entrada_calibre.get())
    dv =0.0
    num_tramos = int(entrada_num_viguetas.get())
    Vu = 0 
    d = h-r-0.01
    
    Analisis_viga(fc,fy,b,h,r,Vu,bv,calibre,dv)
    smaxd, Xvc,xmin, num_est_vc, num_est_min, Vsmax, Vc, Vsreq,long_princ = Analisis_viga(fc,fy,b,h,r,Vu,bv,calibre,dv)
    print(f'Vc_cal {Vc} [kN]')
    print(f'Vsmax_cal {Vsmax} [kN]')

    result_d['text'] = round(d,4)   
    result_Vc['text'] = round(Vc,4)
    result_Vsmax['text'] = round(Vsmax,3)   
    #result_smaxd['text'] = round(smaxd,4)

    global gnum_tramos, gVsmax , gsmaxd, gAsb , gfc, gfy, gb, gh, gr,pos_boton,gbv, gcalibre,gVc, glong_princ
    gnum_tramos = num_tramos
    gVsmax = Vsmax
    gsmaxd = smaxd
    gfc = fc
    gfy = fy
    gb = b
    gh = h
    gr = r
    gbv = bv
    gcalibre = calibre
    gVc = Vc
    glong_princ = long_princ

    boton_tramos.grid_forget()
    boton_regresar.grid_forget()

    pos_boton = 6 + gnum_tramos
    print(gnum_tramos)

    # Actualizamos el label de frame 2 de los aceros
    f2_Vc.config(text=round(gVc,8))
    f2_Vsmax.config(text=round(gVsmax,10))
    #f2_smaxd.config(text=round(gsmaxd,8))

    global entradas
    entradas = {} 

    for i in range(int(gnum_tramos)):  # PARA EL NUMERO DE TRAMOS CREAMOS LAS ENTRADAS DE DE MU, ACERO COLOCADO

        tk.Label(frame2,text=f'tramo {i+1}').grid(row=5+i, column=0, padx=5, pady=3) # Etiqueta de cada tramos 

        entradas[f'Vu_{i}'] = tk.Entry(frame2) # Entrada de Vu de cada tramo
        entradas[f'Vu_{i}'].grid(row=5+i, column=1, padx=5, pady=3) # Vu ingresado
    
        entradas[f'dv_{i}'] = tk.Entry(frame2) # Entrada de acero colocado
        entradas[f'dv_{i}'].grid(row=5+i, column=2, padx=5, pady=3) ## Acero colocado por el usuario

        #tk.Entry(frame2).grid(row=5+i, column=3,padx=7, pady=3 ) # Creamos celdas de entrada de la combinacion de aceros, no se calcula nada con ellas
        #tk.Entry(frame2).grid(row=5+i, column=6,padx=7, pady=3 ) # Creamos celdas de entrada longitudes, no se calcula nada con ellas

    boton_tramos.grid(row=int(pos_boton+2), column=2, padx=5, pady=3)
    boton_regresar.grid(row=int(pos_boton+3), column=3, padx=5, pady=3)



# DEFINO LAS ETIQUETAS DE RUSULTADOS QUE SE ACTUALIZARAN EN EL FRAME 2 con lo calculado en el frame 1 ###################################################33
f2_Vc=tk.Label(frame2, text='  ')
f2_Vc.grid(row=1, column=1, padx=5, pady=3)  # ETIQUETA Vc en frame 2

f2_Vsmax=tk.Label(frame2, text=' ')
f2_Vsmax.grid(row=2, column=1, padx=5, pady=3) # ETIQUETA VS MAX frame 2




boton_calcu1=tk.Button(frame1,text = 'Calcular Capacidad', command=lambda: calculo_aceros()) # Botón para ejecutar la función de lectura de variables
boton_calcu1.grid(row=11, column=1, padx=5, pady=3) # Ubicación en la cuadrícula

boton_cambio_f2=tk.Button(frame1, text='Analisis por viga', command= lambda: mostrar_frame(frame2))
boton_cambio_f2.grid(row=19, column=1, padx=5, pady=3) # Ubicación en la cuadrícula del boton


#################################################  CONTENIDO FRAME 2 ############################################
################################################                     ############################################

tk.Label(frame2, text = ' ANALISIS DE CORTANTE POR TRAMOS').grid(row=0, column=1, columnspan=2, padx=5, pady=3)

##   Traemos los datos de interes ya calculados
tk.Label(frame2, text='Vc [kN]').grid(row=1, column=0, padx=5, pady=3)
tk.Label(frame2, text='Vs max [kN]').grid(row=2, column=0, padx=5, pady=3)
#tk.Label(frame2, text='s max [mm]').grid(row=3, column=0, padx=5, pady=3)


# CREAMOS EL CICLO DE LA CANTIDAD DE VIGUETAS 
#print("Numero de tramos: ", gnum_tramos)


# NOMBRE DE LAS ETIQUETAS INICIALES DE LAS TRAMOS EN EL FRAME 2
tk.Label(frame2, text='Tramo').grid(row=4, column=0, padx=5, pady=3)
tk.Label(frame2, text='Vu [kN]').grid(row=4, column=1, padx=5, pady=3)
tk.Label(frame2, text='long. Cortante [m]').grid(row=4, column=2, padx=5, pady=3)
tk.Label(frame2, text='Vs [kN]').grid(row=4, column=3, padx=5, pady=3)
tk.Label(frame2, text='Chequeo').grid(row=4, column=4, padx=5, pady=3)
tk.Label(frame2, text='Smax diseño [m]').grid(row=4, column=5, padx=5, pady=3)
tk.Label(frame2, text='Long. Refuerzo').grid(row=4, column=6, padx=5, pady=3)
tk.Label(frame2, text='# Estribos').grid(row=4, column=7, padx=5, pady=3)
tk.Label(frame2, text='Long. Refuerzo min').grid(row=4, column=8, padx=5, pady=3)
tk.Label(frame2, text='# Estribos min').grid(row=4, column=9, padx=5, pady=3)
tk.Label(frame2, text='# Total estribos').grid(row=4, column=10, padx=5, pady=3)

global Etiquetas_tramos, Datos_tramos
Datos_tramos ={}
Etiquetas_tramos={}

def calculo_tramos(): # calculamos el diseño por cortante de cada tramo




    for i in range(int(gnum_tramos)):

        Datos_tramos[f'Vu_{i}'] = abs(float(entradas[f'Vu_{i}'].get())) # Vu ingresado
        
        Datos_tramos[f'dv_{i}'] = abs(float(entradas[f'dv_{i}'].get())) # dv ingresado

        smaxd, Xvc,xmin, num_est_vc, num_est_min, Vsmax, Vc, Vsreq ,long_princ = Analisis_viga(gfc,gfy,gb,gh,gr,Datos_tramos[f'Vu_{i}'],gbv,gcalibre,Datos_tramos[f'dv_{i}'])

        #Datos_tramos[f'Asreq_{i}'] = round(Analisis_viga(gfc,gfy,gb,gh,gr,float(Datos_tramos[f'Vu_{i}']))[4],8)

        Datos_tramos[f'Vsreq_{i}'] = round(Vsreq,3)
        Datos_tramos[f'smaxd_{i}'] = round(smaxd,4)
        Datos_tramos[f'long_princ_{i}'] = round(long_princ,3)
        Datos_tramos[f'num_est_vc_{i}'] = num_est_vc

        Datos_tramos[f'xmin_{i}'] = round(xmin,3)

        Datos_tramos[f'num_est_min_{i}'] = num_est_min


        if Vsreq > gVsmax:
            Datos_tramos[f'chequeo_{i}'] = 'NO CUMPLE Vs'
        else:
            Datos_tramos[f'chequeo_{i}'] = 'CUMPLE Vs'

        if f'Vsreq_{i}' in Etiquetas_tramos:
            Etiquetas_tramos[f'Vsreq_{i}'].config(text=f'{Datos_tramos[f"Vsreq_{i}"]}')      
            Etiquetas_tramos[f'chequeo_{i}'].config(text=f'{Datos_tramos[f"chequeo_{i}"]}')       
            Etiquetas_tramos[f'smaxd_{i}'].config(text=f'{Datos_tramos[f"smaxd_{i}"]}')          
            Etiquetas_tramos[f'long_princ_{i}'].config(text=f'{Datos_tramos[f"long_princ_{i}"]}')           
            Etiquetas_tramos[f'num_est_vc_{i}'].config(text=f'{Datos_tramos[f"num_est_vc_{i}"]}')    
            Etiquetas_tramos[f'xmin_{i}'].config(text=f'{Datos_tramos[f"xmin_{i}"]}')   
            Etiquetas_tramos[f'num_est_min_{i}'].config(text=f'{Datos_tramos[f"num_est_min_{i}"]}')   
 

        else:
            Etiquetas_tramos[f'Vsreq_{i}']      = tk.Label(frame2, text=f'{Datos_tramos[f"Vsreq_{i}"]}')
            Etiquetas_tramos[f'Vsreq_{i}'].grid(row=5+i, column=3, padx=5, pady=3)
            Etiquetas_tramos[f'chequeo_{i}']    = tk.Label(frame2, text=f'{Datos_tramos[f"chequeo_{i}"]}')
            Etiquetas_tramos[f'chequeo_{i}'].grid(row=5+i, column=4, padx=5, pady=3)
            Etiquetas_tramos[f'smaxd_{i}']       = tk.Label(frame2, text=f'{Datos_tramos[f"smaxd_{i}"]}')
            Etiquetas_tramos[f'smaxd_{i}'].grid(row=5+i, column=5, padx=5, pady=3)
            Etiquetas_tramos[f'long_princ_{i}']        = tk.Label(frame2, text=f'{Datos_tramos[f"long_princ_{i}"]}')
            Etiquetas_tramos[f'long_princ_{i}'].grid(row=5+i, column=6, padx=5, pady=3)
            Etiquetas_tramos[f'num_est_vc_{i}'] = tk.Label(frame2, text=f'{Datos_tramos[f"num_est_vc_{i}"]}')
            Etiquetas_tramos[f'num_est_vc_{i}'].grid(row=5+i, column=7, padx=5, pady=3)
            Etiquetas_tramos[f'xmin_{i}']       = tk.Label(frame2, text=f'{Datos_tramos[f"xmin_{i}"]}')
            Etiquetas_tramos[f'xmin_{i}'].grid(row=5+i, column=8, padx=5, pady=3)
            Etiquetas_tramos[f'num_est_min_{i}']= tk.Label(frame2, text=f'{Datos_tramos[f"num_est_min_{i}"]}')
            Etiquetas_tramos[f'num_est_min_{i}'].grid(row=5+i, column=9, padx=5, pady=3)
            Etiquetas_tramos[f'total_estri_{i}']= tk.Label(frame2, text=f'{Datos_tramos[f"num_est_min_{i}"]+Datos_tramos[f"num_est_vc_{i}"]}')
            Etiquetas_tramos[f'total_estri_{i}'].grid(row=5+i, column=10, padx=5, pady=3)
        '''
        tk.Label(frame,text=f' {round(Vsreq,3)}').grid(row=5+i, column=3, padx=5, pady=3) # impresion del calculo Asreq
        tk.Label(frame,text=f' {Etiquetas_tramos[f"chequeo_{i}"]}').grid(row=5+i, column=4, padx=5, pady=3) # impresion del calculo Asreq
        tk.Label(frame,text=f' {smaxd}').grid(row=5+i, column=5, padx=5, pady=3) # impresion del calculo Asreq
        tk.Label(frame,text=f' {round(Xvc,4)}').grid(row=5+i, column=6, padx=5, pady=3) # impresion del calculo Asreq
        tk.Label(frame,text=f' {num_est_vc}').grid(row=5+i, column=7, padx=5, pady=3) # impresion del calculo Asreq
        tk.Label(frame,text=f' {round(xmin,4)}').grid(row=5+i, column=8, padx=5, pady=3) # impresion del calculo Asreq
        tk.Label(frame,text=f' {num_est_min}').grid(row=5+i, column=9, padx=5, pady=3) # impresion del calculo Asreq
        '''


boton_tramos=tk.Button(frame2, text='Calculo diseño Cortante ', command= lambda: calculo_tramos())
#boton_tramos.grid(row = pos_boton, column=2, padx=5, pady=3) # Ubicación en la cuadrícula del boton


boton_regresar=tk.Button(frame2, text='Regresar', command= lambda: mostrar_frame(frame1)) 
#boton_regresar.grid(row = pos_boton, column=4, padx=5, pady=3) # Ubicación en la cuadrícula del boton

mostrar_frame(frame1)

ventana1.mainloop()









