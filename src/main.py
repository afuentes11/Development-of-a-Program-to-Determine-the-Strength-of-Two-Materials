import numpy
import csv

## inicialice las variables con los valores correspondientes
RESISTENCIA_1 = 1
RESISTENCIA_2 = 1

LONGITUD = 1
ELASTICIDAD_1 = 1
ELASTICIDAD_2 = 1
AREA_TRANSVERSAL_1 = 1
AREA_TRANSVERSAL_2= 1

incrementos = [x for x in numpy.arange(0, 0.05*26, 0.05)]

# informacion = [["carga maxima"], ["esfuerzo maximo"]]

informacion = {
    "carga_maxima":[],
    "deformacion_maxima": [],
    "deformacion_permanente": [],
    "esfuerzo_residual_1": [],
    "esfuerzo_residual_2": [],
}


for incremento in incrementos:
    
    deformacion_maxima = incremento * RESISTENCIA_2 * (LONGITUD/ELASTICIDAD_2)
    
    esfuerzo_en_parte_elastica_A = RESISTENCIA_1 * (LONGITUD / ELASTICIDAD_1)
    esfuerzo_en_parte_elastica_B = RESISTENCIA_2 * (LONGITUD / ELASTICIDAD_2)
    
    if deformacion_maxima < esfuerzo_en_parte_elastica_A:
        esfuerzo_1 = deformacion_maxima * (LONGITUD / ELASTICIDAD_1)
        esfuerzo_2 = deformacion_maxima * (LONGITUD / ELASTICIDAD_2)
        carga_maxima = (deformacion_maxima/LONGITUD) * (AREA_TRANSVERSAL_1 * ELASTICIDAD_1 + AREA_TRANSVERSAL_2 * ELASTICIDAD_2)
    
    elif esfuerzo_en_parte_elastica_A < deformacion_maxima < esfuerzo_en_parte_elastica_B:
        esfuerzo_1 = RESISTENCIA_1
        esfuerzo_2 = deformacion_maxima * (LONGITUD / ELASTICIDAD_2)
        carga_maxima = AREA_TRANSVERSAL_1 * esfuerzo_1 + (deformacion_maxima*LONGITUD)* (AREA_TRANSVERSAL_2 * ELASTICIDAD_2)
        
    elif deformacion_maxima > esfuerzo_en_parte_elastica_B:
        esfuerzo_1 = RESISTENCIA_1
        esfuerzo_2 = RESISTENCIA_2
        carga_maxima = AREA_TRANSVERSAL_1 * esfuerzo_1 + AREA_TRANSVERSAL_2 * esfuerzo_2


    #deformacion permanente
    pendiente = (AREA_TRANSVERSAL_1 * ELASTICIDAD_1 + AREA_TRANSVERSAL_2 * ELASTICIDAD_2) / LONGITUD
    deformacion_permanente = deformacion_maxima - (carga_maxima / pendiente)
    
    #esfuerzo residual
    esfuerzo_residual_1 = esfuerzo_1 - ((ELASTICIDAD_1 * carga_maxima)/(LONGITUD*pendiente))
    esfuerzo_residual_2 = esfuerzo_2 - ((ELASTICIDAD_2 * carga_maxima)/(LONGITUD*pendiente))
    
    ## almacenamiento de informacion.
    
    informacion["carga_maxima"].append(carga_maxima)
    informacion["deformacion_maxima"].append(deformacion_maxima)
    informacion["deformacion_permanente"].append(deformacion_permanente)
    informacion["esfuerzo_residual_1"].append(esfuerzo_residual_1)
    informacion["esfuerzo_residual_2"].append(esfuerzo_residual_2)



# Definir el nombre del archivo CSV
filename = 'datos.csv'

# Abrir el archivo CSV en modo escritura
with open(filename, 'w', newline='') as f:

    # Crear un objeto writer de CSV
    writer = csv.writer(f)

    # Escribir las cabeceras (nombres de las columnas)
    writer.writerow(informacion.keys())

    # Escribir los datos del diccionario
    writer.writerows(zip(*informacion.values()))
    
print("finalizado")