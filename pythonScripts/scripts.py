import pandas as pd
from datetime import datetime

def transformar_datos(input_file, output_file):
    # Cargar datos originales
    df = pd.read_csv(input_file)
    
    # Verificar columnas requeridas
    required_columns = ['id', 'name', 'company_id', 'amount', 'status', 'created_at', 'paid_at']
    if not all(col in df.columns for col in required_columns):
        missing = set(required_columns) - set(df.columns)
        raise ValueError(f"El archivo CSV no tiene las columnas requeridas. Faltan: {missing}")
    
    # Transformaciones
    df = df.rename(columns={
        'name': 'company_name'
    })
    
    # Asegurar formatos correctos
    df['amount'] = pd.to_numeric(df['amount'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce')
    df['status'] = df['status'].str.lower().str.strip()
    
    # Convertir fechas - manejar diferentes formatos
    try:
        # Primero intentamos con parser ISO8601 completo
        df['created_at'] = pd.to_datetime(df['created_at'], format='ISO8601')
    except ValueError:
        # Si falla, intentamos con formato mixto
        df['created_at'] = pd.to_datetime(df['created_at'], format='mixed')
    
    try:
        # Manejar paid_at que podría tener valores nulos
        df['paid_at'] = pd.to_datetime(df['paid_at'], format='ISO8601', errors='coerce')
    except ValueError:
        df['paid_at'] = pd.to_datetime(df['paid_at'], format='mixed', errors='coerce')
    
    df['updated_at'] = datetime.now()
    
    # Seleccionar y ordenar columnas según el esquema requerido
    result = df[[
        'id', 'company_name', 'company_id', 'amount', 'status', 'created_at', 'paid_at', 'updated_at'
    ]]
    
    # Guardar resultado
    result.to_csv(output_file, index=False)
    print(f"Datos transformados guardados en {output_file}")
    return result

if __name__ == "__main__":
    transformar_datos('DataSet/data_prueba_tecnica.csv', 'DataSet/outputmodif.csv')