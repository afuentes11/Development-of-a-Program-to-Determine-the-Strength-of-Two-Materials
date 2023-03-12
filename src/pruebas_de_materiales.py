import numpy
import csv

def calcular_valores(inicializacion_de_variables: dict) -> dict:
    """
    Calcula la carga máxima, la tensión normal máxima, la deformación permanente y la tensión residual de una pieza de dos 
    materiales diferentes sometida a una carga axial para diferentes valores de incremento.

    Retorna un diccionario con los siguientes valores:
    - carga_maxima (list): una lista con los valores de carga máxima obtenidos para cada incremento.
    - deformacion_maxima (list): una lista con los valores de deformación máxima obtenidos para cada incremento.
    - deformacion_permanente (list): una lista con los valores de deformación permanente obtenidos para cada incremento.
    - esfuerzo_residual_1 (list): una lista con los valores de esfuerzo residual del material 1 obtenidos para cada incremento.
    - esfuerzo_residual_2 (list): una lista con los valores de esfuerzo residual del material 2 obtenidos para cada incremento.

    Parámetros:
    - inicializacion_de_variables (dict): un diccionario que contiene los valores iniciales para las variables de entrada. 

    Retorno:
    Un diccionario con los valores calculados para cada incremento.
    """
    
    ## Inicializacion de las constantes de las resistencias de los materiales 1 y 2
    RESISTENCIA_1 = inicializacion_de_variables["material_1"]["resistencia"]
    RESISTENCIA_2 = inicializacion_de_variables["material_2"]["resistencia"]

    ## inicializacion de la longitud de la pieza
    LONGITUD = inicializacion_de_variables["pieza"]["longitud"]

    ## Inicializacion de los modulos de elasticidad de los materiales 1 y 2
    ELASTICIDAD_1 = inicializacion_de_variables["material_1"]["elasticidad"]
    ELASTICIDAD_2 = inicializacion_de_variables["material_2"]["elasticidad"]

    ## Inicializacion de las areas transversales de los materiales 1 y 2
    AREA_TRANSVERSAL_1 = inicializacion_de_variables["material_1"]["area_transversal"]
    AREA_TRANSVERSAL_2= inicializacion_de_variables["material_2"]["area_transversal"]

    ## Inicializacion de lista de incrementos
    incremento = inicializacion_de_variables["metadata"]["incremento"]
    numero_de_valores = inicializacion_de_variables["metadata"]["numero_de_valores"]
    incrementos = [x for x in numpy.arange(0, incremento * numero_de_valores, incremento)]

    ## inicializacion del diccionario para almacenar la informacion.
    informacion = {
        "carga_maxima":[],
        "deformacion_maxima": [],
        "deformacion_permanente": [],
        "esfuerzo_residual_1": [],
        "esfuerzo_residual_2": [],
    }

    ## iteracion en el numero de valores seleccionado
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
        
    return informacion

def generar_CSV(informacion: dict, nombre_archivo_csv:str ="datos") -> None:
    """
    Genera un archivo CSV a partir de una diccionario de información.

    Parámetros:
    informacion (dict): un diccionario de información que se agregará al archivo CSV.
    nombre_del_archivo (str): el nombre del archivo CSV que se generará. Por defecto es "datos".

    Retorno:
    None
    """
    # Definir el nombre del archivo CSV
    archivo = f'{nombre_archivo_csv}.csv'

    # Abrir el archivo CSV en modo escritura
    with open(archivo, 'w', newline='') as f:

        # Crear un objeto writer de CSV
        escribir = csv.writer(f)

        # Escribir las cabeceras (nombres de las columnas)
        escribir.writerow(informacion.keys())

        # Escribir los datos del diccionario
        escribir.writerows(zip(*informacion.values()))
        
    print("finalizado")
