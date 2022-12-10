import random
import math
import matplotlib.pyplot as plt
import pandas as pd
from statistics import median
from statistics import quantiles
import time

Chargers = 5 # number of particles
Penalty_rate = 0.1 #$/kWh #Penalty for uncharging
Working_hour = range(6,22)
Max_lv2 = 0.1083*15 #charging rate kW h/minute for each PEV
Transformer_capacity = 10.83 # kW h/minute.
precioVenta = 3000 # Precio por megavatio
Medianas = []
LasMedias=[]
Quantiles = []
LCPU=[]
maxF0=[] 
MinimosF0=[]
matriz = pd.DataFrame(columns=['1', '2', '3','4','5','6', '7', '8'],index=range(30))
F0Real=[]#Función objetivo del constructivo por instancia

for instancia in range(6,9): 
    CPU=0
    start=time.time()
    L = pd.read_csv("mai_"+str(instancia).zfill(3)+".txt", sep="	")

    Time_Splot = [
    6, 	6.15, 	6.3, 	6.45, 	7, 	7.15, 	7.3, 	7.45, 	8, 	8.15, 	8.3, 	8.45, 	9, 	9.15, 	9.3, 	9.45, 	
    10, 	10.15, 	10.3, 	10.45, 	11, 	11.15, 	11.3, 	11.45, 	12, 	12.15, 	12.3, 	12.45, 	13, 	13.15, 	
    13.3, 	13.45, 	14, 	14.15, 	14.3, 	14.45, 	15, 	15.15, 	15.3, 	15.45, 	16, 	16.15, 	16.3, 	16.45, 	
    17, 	17.15, 	17.3, 	17.45, 	18, 	18.15, 	18.3, 	18.45, 	19, 	19.15, 	19.3, 	19.45, 	20, 	20.15, 	
    20.3, 	20.45]
    
    # $/Mwh								
    Price ={
    6: 145.285,
    7: 57.2525,
    8: 50.7375,
    9: 21.2375,
    10: 21.3725,
    11: 38.2425,
    12: 57.0275,
    13: 56.14,
    14: 38.4075,
    15: 18.4225,
    16: 49.7325,
    17: 117.6775,
    18: 47.965,
    19: 47.9475,
    20: 32.585,
    21: 38.3325,
    } #Precio por hora by Texas
       
    F0Instancias = [] # Guarda resultados de cada instancia
    listas = []
        
    for u in range(30): # Se generan 30 replicas por intancia
        m=[]
        n=[]
        k=[]
        itera=0
        iterations = 500  # max number of iterations
        Wmin = 0.4 # inertia constant 
        Wmax =0.9  # inertia constant 
        c1 = 2.09  # cognative constant
        c2 = 2.09  # social constant
        Velocity=[]
        particle_position = {									
        6: [0,	0,	0,	0,	0],
        6.15: [0,	0,	0,	0,	0],
        6.3: [0,	0,	0,	0,	0],
        6.45: [0,	0,	0,	0,	0],
        7: [0,	0,	0,	0,	0],
        7.15: [0,	0,	0,	0,	0],
        7.3: [0,	0,	0,	0,	0],
        7.45: [0,	0,	0,	0,	0],
        8: [0,	0,	0,	0,	0],
        8.15: [0,	0,	0,	0,	0],
        8.3: [0,	0,	0,	0,	0],
        8.45: [0,	0,	0,	0,	0],
        9: [0,	0,	0,	0,	0],
        9.15: [0,	0,	0,	0,	0],
        9.3: [0,	0,	0,	0,	0],
        9.45: [0,	0,	0,	0,	0],
        10: [0,	0,	0,	0,	0],
        10.15: [0,	0,	0,	0,	0],
        10.3: [0,	0,	0,	0,	0],
        10.45: [0,	0,	0,	0,	0],
        11: [0,	0,	0,	0,	0],
        11.15: [0,	0,	0,	0,	0],
        11.3: [0,	0,	0,	0,	0],
        11.45: [0,	0,	0,	0,	0],
        12: [0,	0,	0,	0,	0],
        12.15: [0,	0,	0,	0,	0],
        12.3: [0,	0,	0,	0,	0],
        12.45: [0,	0,	0,	0,	0],
        13: [0,	0,	0,	0,	0],
        13.15: [0,	0,	0,	0,	0],
        13.3: [0,	0,	0,	0,	0],
        13.45: [0,	0,	0,	0,	0],
        14: [0,	0,	0,	0,	0],
        14.15: [0,	0,	0,	0,	0],
        14.3: [0,	0,	0,	0,	0],
        14.45: [0,	0,	0,	0,	0],
        15: [0,	0,	0,	0,	0],
        15.15: [0,	0,	0,	0,	0],
        15.3: [0,	0,	0,	0,	0],
        15.45: [0,	0,	0,	0,	0],
        16: [0,	0,	0,	0,	0],
        16.15: [0,	0,	0,	0,	0],
        16.3: [0,	0,	0,	0,	0],
        16.45: [0,	0,	0,	0,	0],
        17: [0,	0,	0,	0,	0],
        17.15: [0,	0,	0,	0,	0],
        17.3: [0,	0,	0,	0,	0],
        17.45: [0,	0,	0,	0,	0],
        18: [0,	0,	0,	0,	0],
        18.15: [0,	0,	0,	0,	0],
        18.3: [0,	0,	0,	0,	0],
        18.45: [0,	0,	0,	0,	0],
        19: [0,	0,	0,	0,	0],
        19.15: [0,	0,	0,	0,	0],
        19.3: [0,	0,	0,	0,	0],
        19.45: [0,	0,	0,	0,	0],
        20: [0,	0,	0,	0,	0],
        20.15: [0,	0,	0,	0,	0],
        20.3: [0,	0,	0,	0,	0],
        20.45: [0,	0,	0,	0,	0],
        }
        vehicle_position = {
        6: [0,	0,	0,	0,	0],
        6.15: [0,	0,	0,	0,	0],
        6.3: [0,	0,	0,	0,	0],
        6.45: [0,	0,	0,	0,	0],
        7: [0,	0,	0,	0,	0],
        7.15: [0,	0,	0,	0,	0],
        7.3: [0,	0,	0,	0,	0],
        7.45: [0,	0,	0,	0,	0],
        8: [0,	0,	0,	0,	0],
        8.15: [0,	0,	0,	0,	0],
        8.3: [0,	0,	0,	0,	0],
        8.45: [0,	0,	0,	0,	0],
        9: [0,	0,	0,	0,	0],
        9.15: [0,	0,	0,	0,	0],
        9.3: [0,	0,	0,	0,	0],
        9.45: [0,	0,	0,	0,	0],
        10: [0,	0,	0,	0,	0],
        10.15: [0,	0,	0,	0,	0],
        10.3: [0,	0,	0,	0,	0],
        10.45: [0,	0,	0,	0,	0],
        11: [0,	0,	0,	0,	0],
        11.15: [0,	0,	0,	0,	0],
        11.3: [0,	0,	0,	0,	0],
        11.45: [0,	0,	0,	0,	0],
        12: [0,	0,	0,	0,	0],
        12.15: [0,	0,	0,	0,	0],
        12.3: [0,	0,	0,	0,	0],
        12.45: [0,	0,	0,	0,	0],
        13: [0,	0,	0,	0,	0],
        13.15: [0,	0,	0,	0,	0],
        13.3: [0,	0,	0,	0,	0],
        13.45: [0,	0,	0,	0,	0],
        14: [0,	0,	0,	0,	0],
        14.15: [0,	0,	0,	0,	0],
        14.3: [0,	0,	0,	0,	0],
        14.45: [0,	0,	0,	0,	0],
        15: [0,	0,	0,	0,	0],
        15.15: [0,	0,	0,	0,	0],
        15.3: [0,	0,	0,	0,	0],
        15.45: [0,	0,	0,	0,	0],
        16: [0,	0,	0,	0,	0],
        16.15: [0,	0,	0,	0,	0],
        16.3: [0,	0,	0,	0,	0],
        16.45: [0,	0,	0,	0,	0],
        17: [0,	0,	0,	0,	0],
        17.15: [0,	0,	0,	0,	0],
        17.3: [0,	0,	0,	0,	0],
        17.45: [0,	0,	0,	0,	0],
        18: [0,	0,	0,	0,	0],
        18.15: [0,	0,	0,	0,	0],
        18.3: [0,	0,	0,	0,	0],
        18.45: [0,	0,	0,	0,	0],
        19: [0,	0,	0,	0,	0],
        19.15: [0,	0,	0,	0,	0],
        19.3: [0,	0,	0,	0,	0],
        19.45: [0,	0,	0,	0,	0],
        20: [0,	0,	0,	0,	0],
        20.15: [0,	0,	0,	0,	0],
        20.3: [0,	0,	0,	0,	0],
        20.45: [0,	0,	0,	0,	0],
        }

        listaDemanda = []
        
# ================== INICIALIZAR MATRIZ P: CONSTRUCTIVO ================================================================================
        for i in range(len(L)): #i=vehiculo
            columna = 0
            entro = False
            CantidadF=math.ceil(L.iloc[i][3]/Max_lv2) #Cantidad de franjas necesarias para suplir la demanda del carro i
            listaDemanda.append(CantidadF)
            j = L.iloc[i][1] #Hora de arribo del vehiculo i
            
        # Validar disponibilidad de cargadores por franja:
            if sum(particle_position[(j)])==Chargers:
                if j-int(j) != 0.45: #Si la franja esta llena, pasa a la sig. franja de 15 min
                    j=j+0.15
                else:                # Si son las y 45, la siguiente franja será en la siguiente hora
                    j=int(j)+1 
            cont=0
            for z in range(int(CantidadF/3)+1): # La z recorre las unidades por hora i.e z=2: 6:00+z = 8:00
                if z==0: #Para asignar en la franja inmediatamente seleccionada que se encontro disponible
                    for w in range(0, round((int(j)+0.45-j)/0.15)+1): #La w recorre las unidades de 15 minutos. i.e si un vehiculo llega a las 6:15, puede aumentar los minutos en esa hora 3 veces(6:15 (w=0), 6:30, 6:45)
                        if w<CantidadF:
                            #round(j+z+0.15*w,2) es la franja que se está evaluando. i.e en la primera iteracion z=0 y w=0 se analiza la franja que e encontro disponble
                            if round(j+z+0.15*w,2) < 21 and cont < ((int(L.iloc[i][2])+(L.iloc[i][2]-int(L.iloc[i][2]))*100/60)-(int(L.iloc[i][1])+(L.iloc[i][1]-int(L.iloc[i][1]))*100/60))/0.25: # Condicion para controlar que NO se pase de las franjas disponibles y que salga a su hora de salida.
                                if entro == False:
                                    for q in range(Chargers):
                                        entro = True
                                        if particle_position[(round(j+z+0.15*w,2))][q] == 0:                                   
                                            columna = q #Guarda la posición del cargador donde se va a asignar el vehiculo
                                            break
                                particle_position[(round(j+z+0.15*w,2))][columna] = 1
                                vehicle_position[(round(j+z+0.15*w,2))][columna] = i+1
                                cont+=1
                        #else:
                            #print("El carro " + str(i+1) + " faltó por cargar " + str((CantidadF-cont)*Max_lv2))
                                
                else: #Para asignar 
                    if cont < CantidadF: #Si aun no se han asignado todas las franjas requeridas a un vehiculo
                        for w in range(0, min(4,CantidadF-cont)): 
                            if round(int(j)+z+0.15*w,2) < 21 and cont < ((int(L.iloc[i][2])+(L.iloc[i][2]-int(L.iloc[i][2]))*100/60)-(int(L.iloc[i][1])+(L.iloc[i][1]-int(L.iloc[i][1]))*100/60))/0.25:
                                particle_position[(round(int(j)+z+0.15*w,2))][columna] = 1
                                vehicle_position[(round(int(j)+z+0.15*w,2))][columna] = i+1
                                cont+=1
                            # else:
                            #     print("El carro " + str(i+1) + " faltó por cargar " + str((CantidadF-cont)*Max_lv2))
# =======================================================================================================================================        
        
        ocup = [] # Franjas ocupadas por cargador en el constructivo
        for i in range(Chargers):
            ocupacion = 0 # Ocupación por cargador
            for j in Time_Splot:
                ocupacion = ocupacion + particle_position[j][i]
            ocup.append(ocupacion)
                 
            
        F0 = [] # Función objetivo del constructivo por cargador en $/Mwh
        
        real=0
        for i in range(Chargers):
            objetivo = 0
            for j in Time_Splot:
                objetivo = objetivo + (particle_position[j][i]*Max_lv2*0.001*precioVenta - particle_position[j][i]*Price[int(j)]*Max_lv2*0.01) # Calcula función objetivo pasando a megavoltios      
                real=real+(particle_position[j][i]*Max_lv2*0.001*precioVenta - particle_position[j][i]*Price[int(j)]*Max_lv2*0.001)
            F0.append(objetivo)
        
        #Matriz de velocidades inicial generada aleatoriamente
        particle_velocity = {				
        0: [0, 	0, 	1, 	0, 	0, 	0, 	1, 	1, 	1, 	0, 	0, 	0, 	0, 	1, 	1, 	1, 	0, 	1, 	0, 	1, 	0, 	0, 	0, 	1, 	0, 	1, 	0, 	1, 	0, 	0, 	0, 	0, 	1, 	1, 	0, 	0, 	0, 	0, 	0, 	1, 	0, 	1, 	0, 	0, 	1, 	1, 	0, 	1, 	1, 	1, 	1, 	1, 	1, 	1, 	1, 	1, 	1, 	1, 	1, 	0],
        1: [0, 	0, 	1, 	0, 	1, 	0, 	1, 	0, 	1, 	0, 	0, 	0, 	0, 	0, 	0, 	0, 	0, 	1, 	1, 	0, 	1, 	1, 	0, 	0, 	1, 	0, 	0, 	0, 	0, 	0, 	1, 	1, 	1, 	0, 	0, 	0, 	1, 	0, 	1, 	1, 	1, 	0, 	1, 	1, 	0, 	1, 	1, 	0, 	1, 	0, 	1, 	1, 	0, 	1, 	1, 	0, 	0, 	1, 	0, 	1],
        2: [0, 	1, 	1, 	0, 	0, 	1, 	1, 	0, 	1, 	0, 	0, 	1, 	0, 	0, 	0, 	1, 	1, 	0, 	1, 	0, 	0, 	1, 	1, 	0, 	1, 	0, 	0, 	0, 	0, 	0, 	1, 	1, 	0, 	0, 	1, 	1, 	1, 	0, 	1, 	0, 	0, 	0, 	1, 	1, 	1, 	0, 	0, 	1, 	1, 	0, 	1, 	0, 	0, 	0, 	0, 	1, 	1, 	0, 	1, 	1],
        3: [1, 	1, 	1, 	1, 	0, 	0, 	0, 	0, 	1, 	1, 	1, 	0, 	0, 	1, 	0, 	0, 	0, 	0, 	0, 	0, 	0, 	0, 	0, 	1, 	0, 	1, 	1, 	0, 	0, 	1, 	1, 	1, 	0, 	1, 	1, 	1, 	1, 	1, 	1, 	0, 	0, 	0, 	0, 	1, 	0, 	1, 	0, 	0, 	0, 	1, 	0, 	0, 	1, 	1, 	1, 	1, 	0, 	0, 	0, 	0],
        4: [1, 	1, 	1, 	0, 	0, 	1, 	0, 	0, 	0, 	0, 	0, 	1, 	0, 	1, 	0, 	1, 	0, 	0, 	1, 	1, 	0, 	0, 	1, 	0, 	0, 	1, 	0, 	0, 	0, 	1, 	1, 	0, 	1, 	1, 	0, 	1, 	0, 	0, 	0, 	0, 	1, 	1, 	0, 	0, 	1, 	0, 	1, 	0, 	0, 	0, 	0, 	1, 	1, 	0, 	0, 	1, 	1, 	0, 	0, 	0]
        }
    
    
# =============== ITERACIONES PSO =============================================================================================================
    
        P_best = particle_position.copy()
        F0_best = F0[:] # Función objetivo de cada cargador
        Charger_best = list.index(F0, max(F0)) 
        G_best=[]
        for i in Time_Splot:
            G_best.append(particle_position[i][Charger_best])#Guarda la asignación del mejor cargador
            
        F_Gbest = max(F0_best)
        
        for h in range(iterations):
            
            # Definir vectores r1 y r2
            r1=[]
            r2=[]
            for i in range(len(Time_Splot)):
                r1.append(random.random())
                r2.append(random.random())
            
            itera += 1
            w = Wmax - (Wmax-Wmin)*(itera/iterations)**2    
            
            for j in range(Chargers): 
            # Calcular la nueva velocidad de la partícula
                P_bestj = []
                particle_positionj = []
                # Para utilizar las columnas (por cargador) y no las filas:
                for i in Time_Splot:
                    P_bestj.append(P_best[i][j]) # Guardar la lista por cargador del P_best
                    particle_positionj.append(particle_position[i][j]) # Guarda la lista por cargador del particle_position
                
                cognitive_velocity = [a*b for a,b in zip([n * c1 for n in r1], list(map(lambda x,y: x-y ,P_bestj,particle_positionj)))]
                social_velocity = [a*b for a,b in zip([n * c2 for n in r2], list(map(lambda x,y: x-y ,G_best,particle_positionj)))]
                
                particle_velocity[j] = list(map(lambda x,y: x+y ,[n * w for n in particle_velocity[j]], list(map(lambda x,y: x+y ,cognitive_velocity,social_velocity))))      
                
            # Calcular la nueva posición de la partícula
                for i in Time_Splot:
                    particle_position[i][j] = particle_position[i][j] + particle_velocity[j][list.index(Time_Splot,i)]
                    # Poner la matriz en 0's y 1's
                    if particle_position[i][j] < 0.5:
                        particle_position[i][j]=0 
                    else:
                        particle_position[i][j]=1
            
        # Arreglar matrices según la cantidad de 1's que debe haber en cada cargador
            ocupTemp = [] # Vector de ocupación por cargador
            listaPosicionesUnos = []
            listaPosicionesCeros = []
            for i in range(Chargers): # Suma las ocupación por cargador en la matriz obtenida
                ocupacionTemp = 0 # Ocupación por cargador
                posicionesUnos = []
                posicionesCeros = []
                for j in Time_Splot:
                    ocupacionTemp = ocupacionTemp + particle_position[j][i]
                    if particle_position[j][i] == 1:
                        posicionesUnos.append(j)
                    else:
                        posicionesCeros.append(j)
                ocupTemp.append(ocupacionTemp)
                listaPosicionesUnos.append(posicionesUnos)
                listaPosicionesCeros.append(posicionesCeros)
            
            diferencia = list(map(lambda x,y: x-y ,ocupTemp,ocup)) #Diferencia entre la ocupación del constructivo  del PSO
            
            # Poner o quitar 1's teniendo en cuenta la restricción de demanda
            for i in range(Chargers):
                for a in range(abs(diferencia[i])):
                    if diferencia[i]<0: #Si a la solución le faltan 1's
                        aleatorio = random.choice(listaPosicionesCeros[i]) #Seleccionar un 0 para cambiarlo por un 1
                        particle_position[aleatorio][i]=1
                        listaPosicionesCeros[i].remove(aleatorio)
                    elif diferencia[i]>0: # Si a la solución le sobran 1's
                        aleatorio = random.choice(listaPosicionesUnos[i]) #Seleccionar un 1 para cambiarlo por un 0
                        particle_position[aleatorio][i]=0
                        listaPosicionesUnos[i].remove(aleatorio)
                      
            # Actualizar Pbest y F0_best
            F0 = []
            F0Sin = []
            for w in range(Chargers):
                objetivo = 0
                for q in Time_Splot:
                    objetivo = objetivo + (particle_position[q][w]*Max_lv2*0.001*precioVenta) - (particle_position[q][w]*Price[int(q)]*Max_lv2*0.001) - (abs(diferencia[w])/540) # Calcula función objetivo pasando a megavoltios. Se penaliza la función con la diferencia por franja (60)   
                F0.append(objetivo)
                insertar = F0[w]
                if insertar > F0_best[w]:
                    F0_best[w] = insertar # Guarda valor de F0 para esa columna
                    for i in Time_Splot:
                        P_best[i][w] = particle_position[i][w] # Guarda columna que genera ese valor de F0
                        
            # Graficar F0 sin penalizar
            objetivoP = 0
            for s in range(Chargers):
                for c in Time_Splot:
                    objetivoP = objetivoP + (P_best[c][s]*Max_lv2*0.001*precioVenta) - (P_best[c][s]*Price[int(c)]*Max_lv2*0.001)
            
            m.append(int(itera))
            n.append(objetivoP) # No penalizadasS
            
            #Actualizar G_best y FG_best
            if max(F0_best) > F_Gbest:
                F_Gbest = max(F0_best) # Mejor F0 global
                Charger_best = list.index(F0_best, max(F0_best)) # Franja que genera mejor F0 global
                G_best=[]
                for i in Time_Splot:
                    G_best.append(particle_position[i][Charger_best]) # Vector 0's y 1's que está en la mejor columna
            
            
            k.append(sum(F0_best))
        plt.title("Objective function of iteration "+str(instancia))
        plt.xlabel('Iteration')
        plt.ylabel('Objective Function') 
        plt.plot(m,k,":")
        plt.show()
        print("FO PSO: " + str(max(k)))
        listas.append(k)
        
    
        F0Instancias.append(max(n)) #Vector de 30 F0s
        matriz.iloc[u][instancia-1] = max(n)
    
    
    # ======================================    
    # CALCULO DE ESTADÍSTICAS COMPARATIVAS
    # ======================================
    F0Real.append(real) #Función objetivo del constructivo de cada instancia
    end = time.time()
    CPU =(end-start)
    LCPU.append(CPU)
    maxF0.append(max(F0Instancias)) #mejor F0 de cada iteración, se compara con la F0 inicial
    MinimosF0.append(min(F0Instancias)) #El menor valor de las 30 replicas(de los mejores encontrados en cada replica) para cada instancia 
    media = sum(F0Instancias)/len(F0Instancias)
    LasMedias.append(media)
    # ----- Mediana -----
    mediana = median(F0Instancias) #Muestra la media por cada instancia (2000 replicas porcada instancia)
    Medianas.append(mediana)
    quantil=quantiles(F0Instancias)
    Quantiles.append(quantil)
    


#----- Quantil_Instancia 8 -----
columna=[]
for fila in range(len(matriz)):
    columna.append(matriz.iloc[fila][7])
    
fig = plt.figure(figsize =(10, 7)) 
for i in range(2):
    plt.boxplot(columna)
plt.title("Iteration 8")    
plt.show
