
# librerias
import tkinter as tk 
import numpy as np # import array, roots,around, zeros
#from sympy import symbols, solve    
from math import sqrt

# creamos ventana principal

def mostrar_frame(frame):
    frame.tkraise() ## trae al frame que sea llamado


def acero_colocado(combi):
    as_colocado = 0

    combinacioanes = combi.split('+') # Separamos por el simbolo + para obtener cada combinacion de acero

    for combinacion in combinacioanes:
        combinacion = combinacion.strip() # Eliminamos espacios en blanco
        if '#' in combinacion:
            num_barras , calibre = combinacion.split('#')
            as_colocado += float(num_barras)*lista_refuerzo[int(calibre),2]/1000000
        else:
            as_colocado += eval(combinacion)/10000  # Si no hay #, evaluamos la expresión directamente (cambiamos a m2 para realizar comparativa)
    return as_colocado



def Analisis_viga(fc,fy,b,h,r,Mu):
    # Vamos a asumir que phi = 0.9 dado que diseñamos para que trabajen controladas por traccion
    phi = 0.9
    # Asumimos acero de E = 200GPa
    E = 200000*1000 # KPa
    ey = fy/E
    euc = 0.003
    es = euc + ey # Definimos deformacion deseada del acero
    d = h - r - 0.01 # Altura efectiva

    print(f"fc = {round(fc,3)} [kPa]")
    print(f"fy = {round(fy,3)} [kPa]")
    print(f"b = {round(b,3)} [m]")
    print(f"h = {round(h,3)} [m]")
    print(f"r = {round(r,3)} [m]")
    print(f"Mu = {round(Mu,3)} [kN*m]")
    print(f"ey = {round(ey,5)} [m/m]")


    # Calculamos acero minimo
    As_m1 =0.25*sqrt(fc/1000)*b*d/(fy/1000)
    As_m2 = 1.4*b*d/(fy/1000)
    As_min = max(As_m1, As_m2) # Acero minimo requerido

    # Calculamos B1 segun f'c
    if fc/1000 >= 17:
        if fc/1000 < 28:
            B1 = 0.85
        elif fc/1000 < 56:
            B1 = 0.85-0.05*(fc/1000-28)/7
        else:
            B1 = 0.65
    else: 
       print("Defina un fc valido")        
    print("B1 = ", B1)


    # Acero balanceado
    cb = euc*d/(euc+ey)  # Eje neutro balanceado
    Asb = 0.85*fc*cb*B1*b/fy  # Area acero balanceado

    # Acero maximo

    AsmaxNSR = (0.85*fc*B1*b)*(d*euc/(euc+0.004))/fy
    Asmax = 0.85*fc*B1*b*(d*euc/(euc+(ey+euc)))/fy
   
    ## ACERO REQUERIDO para ser controlada por traccion
    if ((-phi*b*d*fy*fc)**2-4*phi*0.59*(fy**2)*(fc*Mu*b)) <= 0:

        print("No es posible calcular As requerido, revise los datos ingresados")
        Asreq = 0
    else:
        Asreq = (-(-phi*b*d*fy*fc)-sqrt((-phi*b*d*fy*fc)**2-4*phi*0.59*(fy**2)*(fc*Mu*b)))/(2*phi*0.59*fy**2)

    print(f"Acero minimo = {round(As_min,7)} [m2]")
    print(f"Acero balanceado = {round(Asb,7)} [m2]")
    print(f"Acero maximo NSR = {round(AsmaxNSR,7)} [m2]")
    print(f"Acero maximo = {round(Asmax,7)} [m2]")
    #print(f"Acero requerido = {round(Asreq,7)} [m2]")
    print('    ')

    return As_min, Asb, AsmaxNSR, Asmax, Asreq


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


ventana1 = tk.Tk()
ventana1.geometry("900x600") ## tamaño de la ventana general
ventana1.title("DISEÑO A FLEXION NSR-10") ## titulo de la ventana general

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



etiq_inicio = tk.Label(frame1, text='Welcome to free design -- by Andres Villaquirán ')
etiq_inicio.grid(row=0, column=0, columnspan=3, padx=5, pady=3)


etiq_ing_valores = tk.Label(frame1, text='Ingreso de parametro de la viga')
etiq_raviso = tk.Label(frame1, text='Si hay estribos sumar diametro a el recubrimiento')
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

etiq_h = tk.Label(frame1, text='h [m]')
entrada_h  = tk.Entry(frame1)
etiq_h.grid(row=5, column=0, padx=5, pady=3) # Ubicación en la cuadrícula
entrada_h.grid(row=5, column=2, padx=3, pady=3) # Ubicación en la cuadrícula


etiq_r = tk.Label(frame1, text='r [m]')
entrada_r  = tk.Entry(frame1)
etiq_r.grid(row=6, column=0, padx=10, pady=3) # Ubicación en la cuadrícula
entrada_r.grid(row=6, column=2, padx=3, pady=3) # Ubicación en la cuadrícula

#etiq_Mu = tk.Label(frame1, text='Mu [kN-m]')
#entrada_Mu = tk.Entry(frame1)
#etiq_Mu.grid(row=7, column=0, padx=10, pady=3) # Ubicación en la cuadrícula
#entrada_Mu.grid(row=7, column=2, padx=3, pady=3) # Ubicación en la cuadrícula

## ventanas de resultados

etiq_d = tk.Label(frame1,text='d [m]')
etiq_d.grid(row=12, column=0, padx=5, pady=3) # Ubicación en la cuadrícula

etiq_As_min = tk.Label(frame1,text='As min [cm2]')
etiq_As_min.grid(row=13, column=0, padx=5, pady=3) # Ubicación en la cuadrícula

etiq_Asb = tk.Label(frame1,text='As balanceado [cm2]')
etiq_Asb.grid(row=14, column=0, padx=5, pady=3) # Ubicación en la cuadrícula

etiq_AsmaxNSR = tk.Label(frame1,text='As max NSR [cm2]')
etiq_AsmaxNSR.grid(row=15, column=0, padx=5, pady=3) # Ubicación en la cuadrícula

etiq_Amax = tk.Label(frame1,text='As max [cm2]')         
etiq_Amax.grid(row=16, column=0, padx=5, pady=3) # Ubicación en la cuadrícula

#etiq_Asreq = tk.Label(frame1,text='As requerido [cm2]')      
#etiq_Asreq.grid(row=16, column=0, padx=5, pady=3) # Ubicación en la cuadrícula

#etiq_tipo = tk.Label(frame1,text='Control')      
#etiq_tipo.grid(row=16, column=0, padx=5, pady=3) # Ubicación en la cuadrícula

etiq_num_viguetas = tk.Label(frame1, text='Numero de tramos')
etiq_num_viguetas.grid(row=8, column =0, padx=5, pady=3) # Ubicación en la cuadrícula

entrada_num_viguetas = tk.Entry(frame1)
entrada_num_viguetas.grid(row=8, column =2, padx=5, pady=3)

## Etiqueta de resultados


result_d = tk.Label(frame1)
result_d.grid(row=12, column=2, padx=5, pady=3) # 

result_As_min = tk.Label(frame1)
result_As_min.grid(row=13, column=2, padx=5, pady=3) # 

result_Asb = tk.Label(frame1)
result_Asb.grid(row=14, column=2, padx=5, pady=3) # 

result_AsmaxNSR = tk.Label(frame1)
result_AsmaxNSR.grid(row=15, column=2, padx=5, pady=3) # 

result_Asmax = tk.Label(frame1)         
result_Asmax.grid(row=16, column=2, padx=5, pady=3) # 

#result_Asreq = tk.Label(frame1)      
#result_Asreq.grid(row=16, column=2, padx=5, pady=3) # 

#result_tipo = tk.Label(frame1)      
#result_tipo.grid(row=16, column=2, padx=5, pady=3) # 


def calculo_entradas():   # Leemos las variables que entraron al principio

    fc = float(entrada_fc.get())*1000 # Convertimos a KPa
    fy = float(entrada_fy.get())*1000 # Convertimos a KPa
    b = float(entrada_b.get())
    h = float(entrada_h.get())
    r = float(entrada_r.get())
    # Mu = float(entrada_Mu.get())
    Mu = 0
    d = h-r-0.01
    num_tramos = int(entrada_num_viguetas.get())

    print

    
    Analisis_viga(fc,fy,b,h,r,Mu)
    As_min, Asb, AsmaxNSR, Asmax, Asreq = Analisis_viga(fc,fy,b,h,r,Mu)

    result_d['text'] = round(d,5)   
    result_As_min['text'] = round(As_min*10000,4)
    result_Asb['text'] = round(Asb*10000,3)
    result_AsmaxNSR['text'] = round(AsmaxNSR*10000,3)
    result_Asmax['text'] = round(Asmax*10000,3)
    #result_Asreq['text'] = round(Asreq,8)
    ''''
    if Asreq > Asb:
        result_tipo['text'] = 'Compresion No cumple'
    elif Asreq > Asmax: 
        result_tipo['text'] = 'Transicion'
    else:
        result_tipo['text'] = 'Tracción'
    '''
    global gnum_tramos, gAsmax , gAsmin, gAsb , gfc, gfy, gb, gh, gr,pos_boton
    gnum_tramos = num_tramos
    gAsmax = Asmax
    gAsmin = As_min
    gAsb = Asb
    gfc = fc
    gfy = fy
    gb = b
    gh = h
    gr = r

    boton_tramos.grid_forget()
    boton_regresar.grid_forget()
    boton_evaluar.grid_forget()

    pos_boton = 6 + gnum_tramos
    print(gnum_tramos)

    # Actualizamos el label de frame 2 de los aceros
    f2_Asmax.config(text=round(gAsmax*10000,3))
    f2_Asmin.config(text=round(gAsmin*10000,3))

    global entradas, etiquetas_asreq, etiquetas_eval
    entradas = {} 
    etiquetas_asreq ={ }
    etiquetas_eval ={ }

    for i in range(int(gnum_tramos)):
    
        # Creas la etiqueta una sola vez y la guardas en el diccionario
        lbl = tk.Label(frame2, text="")
        lbl.grid(row=5+i, column=2, padx=5, pady=3)
        etiquetas_asreq[f'Asreq_{i}'] = lbl

        lbl_eval = tk.Label(frame2, text="")
        lbl_eval.grid(row=5+i, column=5, padx=5, pady=3)
        etiquetas_eval[f'evaluacionAsq_{i}'] = lbl_eval

    for i in range(int(gnum_tramos)):  # PARA EL NUMERO DE TRAMOS CREAMOS LAS ENTRADAS DE DE MU, ACERO COLOCADO

        tk.Label(frame2,text=f'tramo {i+1}').grid(row=5+i, column=0, padx=5, pady=3) # Etiqueta de cada tramos 

        entradas[f'Mu_{i}'] = tk.Entry(frame2) # Entrada de Mu de cada tramo
        entradas[f'Mu_{i}'].grid(row=5+i, column=1, padx=5, pady=3) # Mu ingresado
    

        entradas[f'Combinacion_{i}']  = tk.Entry(frame2) # Entrada de acero colocado
        entradas[f'Combinacion_{i}'].grid(row=5+i, column=3, padx=5, pady=3) ## Acero colocado por el usuario
       
      
        #tk.Entry(frame2).grid(row=5+i, column=3,padx=7, pady=3 ) # Creamos celdas de entrada de la combinacion de aceros, no se calcula nada con ellas
        tk.Entry(frame2).grid(row=5+i, column=6,padx=7, pady=3 ) # Creamos celdas de entrada longitudes, no se calcula nada con ellas

    boton_tramos.grid(row=int(pos_boton+2), column=2, padx=5, pady=3)
    boton_regresar.grid(row=int(pos_boton+3), column=3, padx=5, pady=3)
    boton_evaluar.grid(row = int(pos_boton+2), column=4, padx=5, pady=3) # Ubicación en la cuadrícula del boton



# DEFINO LAS ETIQUETAS DE RUSULTADOS QUE SE ACTUALIZARAN EN EL FRAME 2 con lo calculado en el frame 1 ###################################################33
f2_Asmax=tk.Label(frame2, text='  ')
f2_Asmax.grid(row=1, column=1, padx=5, pady=3)  # ETIQUETA AS MAX en frame 2

f2_Asmin=tk.Label(frame2, text=' ')
f2_Asmin.grid(row=1, column=3, padx=5, pady=3) # ETIQUETA AS MIN frame 2



boton_calcu1=tk.Button(frame1,text = 'Calcular', command=lambda: calculo_entradas()) # Botón para ejecutar la función de lectura de variables
boton_calcu1.grid(row=11, column=1, padx=5, pady=3) # Ubicación en la cuadrícula

boton_cambio_f2=tk.Button(frame1, text='Analisis por viga', command= lambda: mostrar_frame(frame2))
boton_cambio_f2.grid(row=19, column=1, padx=5, pady=3) # Ubicación en la cuadrícula del boton


#################################################  CONTENIDO FRAME 2 ############################################
################################################                     ############################################

tk.Label(frame2, text = ' ANALISIS DE FLEZION POR MOMENTOS').grid(row=0, column=1, columnspan=2, padx=5, pady=3)

##   Traemos los datos de interes ya calculados
tk.Label(frame2, text='As max [cm2]').grid(row=1, column=0, padx=5, pady=3)
tk.Label(frame2, text='As min [cm2]').grid(row=1, column=2, padx=5, pady=3)
#tk.Label(frame2, text=' En [Combianción] use (num_barras#calibre) o valor en [cm2]').grid(row=2, column=2, columnspan=4,padx=5, pady=3)


# CREAMOS EL CICLO DE LA CANTIDAD DE VIGUETAS 
#print("Numero de tramos: ", gnum_tramos)


# NOMBRE DE LAS ETIQUETAS INICIALES DE LAS TRAMOS EN EL FRAME 2
tk.Label(frame2, text='Tramo').grid(row=4, column=0, padx=5, pady=3)
tk.Label(frame2, text='Mu [kN-m]').grid(row=4, column=1, padx=5, pady=3)
tk.Label(frame2, text='As requerido [cm2]').grid(row=4, column=2, padx=5, pady=3)
tk.Label(frame2, text='Combinacion').grid(row=4, column=3, padx=5, pady=3)
tk.Label(frame2, text='As colocado').grid(row=4, column=4, padx=5, pady=3)
tk.Label(frame2, text='Evaluacion').grid(row=4, column=5, padx=5, pady=3)
tk.Label(frame2, text='Longitud').grid(row=4, column=6, padx=5, pady=3)


def calculo_tramos(): # calculamos el acero requerido con el momento ingresado

    global Datos_tramos , gnum_tramos
    Datos_tramos ={}


    for i in range(int(gnum_tramos)):

        Datos_tramos[f'Mu_{i}'] = abs(float(entradas[f'Mu_{i}'].get())) # Mu ingresado

        Datos_tramos[f'Asreq_{i}'] = round(Analisis_viga(gfc,gfy,gb,gh,gr,float(Datos_tramos[f'Mu_{i}']))[4],8) # calculamos el acero requerido
        
        if Datos_tramos[f'Asreq_{i}'] == 0:
            aviso_Asreq = "Rev. Seccion"
        else:
            aviso_Asreq = round(Datos_tramos[f'Asreq_{i}']*10000, 3)

        etiquetas_asreq[f'Asreq_{i}'].config(text=f'{aviso_Asreq}')  # Actualizamos el texto de la etiqueta de Asreq
     

def evaluar_Asreq():

    for i in range(int(gnum_tramos)):
            
        Datos_tramos[f'Acero_colocado_{i}'] = acero_colocado(entradas[f'Combinacion_{i}'].get()) # calculamos el acero colocado con la función de acero colocado y la combinacion ingresada por el usuario
         
        #Datos_tramos[f'Acero_colocado_{i}'] = float(entradas[f'Acero_colocado_{i}'].get())
        #Datos_tramos[f'Acero_colocado_{i}'] = eval(entradas[f'Acero_colocado_{i}'].get())

        if gAsmin > gAsmax:
            texto = 'NO CUMPLE' 

        elif float(Datos_tramos[f'Asreq_{i}']) > gAsmax:

            #Datos_tramos[f'evaluacionAsq_{i}'] = tk.Label(frame2,text='NO CUMPLE')
            #Datos_tramos[f'evaluacionAsq_{i}'].grid(row=5+i, column=4, padx=5, pady=3) 
            texto = 'NO CUMPLE' 

        elif float(Datos_tramos[f'Acero_colocado_{i}']) > gAsmax:

            #Datos_tramos[f'evaluacionAsq_{i}'] = tk.Label(frame2,text='NO CUMPLE')
            #Datos_tramos[f'evaluacionAsq_{i}'].grid(row=5+i, column=4, padx=5, pady=3)
            texto = 'NO CUMPLE'
        
        elif float(Datos_tramos[f'Acero_colocado_{i}']) < Datos_tramos[f'Asreq_{i}']:

            #Datos_tramos[f'evaluacionAsq_{i}']= tk.Label(frame2,text='CUMPLE')
            #Datos_tramos[f'evaluacionAsq_{i}'].grid(row=5+i, column=4, padx=5, pady=3)
            texto = ' NO CUMPLE' 

        elif  float(Datos_tramos[f'Asreq_{i}']) < gAsmin:
            #Datos_tramos[f'evaluacionAsq_{i}']= tk.Label(frame2,text='USE AS MIN')
            #Datos_tramos[f'evaluacionAsq_{i}'].grid(row=5+i, column=4, padx=5, pady=3)
            texto = 'USE AS MIN'

        else:
            #Datos_tramos[f'evaluacionAsq_{i}'] = tk.Label(frame2,text='CUMPLE')
            #Datos_tramos[f'evaluacionAsq_{i}'].grid(row=5+i, column=4, padx=5, pady=3)
            texto = 'CUMPLE'

        etiquetas_eval[f'evaluacionAsq_{i}'].config(text=texto) # actualizamos el texto de la etiqueta

#        if f'evaluacionAsq_{i}' in Datos_tramos:
#
#            #Datos_tramos[f'evaluacionAsq_{i}'].destroy() # eliminamos la etiqueta
#            Datos_tramos[f'evaluacionAsq_{i}'].config(text=texto) # actualizamos el texto de la etiqueta
#        else:
#            Datos_tramos[f'evaluacionAsq_{i}'] = tk.Label(frame2,text=texto)
#           Datos_tramos[f'evaluacionAsq_{i}'].grid(row=5+i, column=5, padx=5, pady=3)


        if f'etiq_Ascolomado_{i}' in Datos_tramos:

            #Datos_tramos[f'evaluacionAsq_{i}'].destroy() # eliminamos la etiqueta
            Datos_tramos[f'etiq_Ascolomado_{i}'].config(text=f'{round(Datos_tramos[f'Acero_colocado_{i}']*10000, 3)}') # actualizamos el texto de la etiqueta
        else:
            Datos_tramos[f'etiq_Ascolomado_{i}'] = tk.Label(frame2,text=f'{round(Datos_tramos[f'Acero_colocado_{i}']*10000, 3)}')
            Datos_tramos[f'etiq_Ascolomado_{i}'].grid(row=5+i, column=4, padx=5, pady=3)


       # tk.Label(frame2, text=f'{round(Datos_tramos[f'Acero_colocado_{i}']*10000, 3)}'). grid(row =5+i , column = 4, padx=5, pady=3)



boton_tramos=tk.Button(frame2, text='Calcular Asreq ', command= lambda: calculo_tramos())
#boton_tramos.grid(row = pos_boton, column=2, padx=5, pady=3) # Ubicación en la cuadrícula del boton

boton_evaluar=tk.Button(frame2, text='Evaluar Acero', command= lambda: evaluar_Asreq()) 
#boton_evaluar.grid(row = pos_boton, column=3, padx=5, pady=3) # Ubicación en la cuadrícula del boton


boton_regresar=tk.Button(frame2, text='Regresar', command= lambda: mostrar_frame(frame1)) 
#boton_regresar.grid(row = pos_boton, column=4, padx=5, pady=3) # Ubicación en la cuadrícula del boton

mostrar_frame(frame1)

ventana1.mainloop()






