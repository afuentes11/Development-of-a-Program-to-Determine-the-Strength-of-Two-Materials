from src import pruebas_de_materiales

NOMBRE_ARCHIVO_CSV = "datos"
INICIALIZACION_VARIABLES = {
    
    "material_1":{
        "resistencia":1,
        "elasticidad":1,
        "area_transversal":1
    },
    
    "material_2":{
        "resistencia":1,
        "elasticidad":1,
        "area_transversal":1
    },
    
    "pieza":{
        "longitud":1
    },
    
    "metadata":{
        "incremento":0.05,
        "numero_de_valores":25
    }
    
}

def main():
    informacion = pruebas_de_materiales.calcular_valores(INICIALIZACION_VARIABLES)
    pruebas_de_materiales.generar_CSV(informacion, nombre_archivo_csv = NOMBRE_ARCHIVO_CSV)

if __name__ == "__main__":
    main()