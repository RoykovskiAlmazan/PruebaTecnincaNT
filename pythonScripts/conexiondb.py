import mysql.connector
from mysql.connector import Error
from datetime import datetime
import pandas as pd
import re

def cargarDatos():
    conexion = None  # Inicializar la variable para evitar UnboundLocalError
    try:
        # 1. Leer el archivo CSV
        dataset = pd.read_csv('DataSet/outputmodif.csv')

        def limpiar_amount(values):
            if pd.isna(values):
                return None
            try:
                cleaned = re.sub(r'[^\d.-]', '', str(values))
                amount = float(cleaned)

                if -999999999999999.99 <= amount <= 999999999999999.99:
                    return round(amount, 2)
                return None
            except:
                return
        dataset['amount'] = dataset['amount'].apply(limpiar_amount)
        dataset = dataset.dropna(subset=['id'])
        dataset = dataset[dataset['id'].astype(str).str.strip() != '']
        # 2. Convertir NaN a None - FORMA CORRECTA
        dataset = dataset.where(pd.notna(dataset), None)
        
        # 3. Conectar a MySQL
        conexion = mysql.connector.connect(
            host='localhost',
            database='EmpresaPTNT',
            user='admin',
            password='1234')
            
        if conexion.is_connected():
            cursor = conexion.cursor()
            
            # 4. Insertar companies (nota: usas 'companie_id' en la tabla)
            companies_data = dataset[['company_id', 'company_name']].drop_duplicates()
            
            for _, row in companies_data.iterrows():
                if row['company_id'] is None:  # Manejar valores nulos
                    continue
                
                cursor.execute("""
                    INSERT INTO companies (companie_id, companie_name, created_at) 
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                    companie_name = VALUES(companie_name)
                """, (row['company_id'], row['company_name'], datetime.now()))
            
            # 5. Insertar charges
            for _, row in dataset.iterrows():
                if row['company_id'] is None:  # Validar clave foránea
                    continue
                
                paid_at = row['paid_at'] if pd.notna(row['paid_at']) else None
                
                cursor.execute("""
                    INSERT INTO charges (id, company_id, amount, status, created_at, paid_at, updated_at) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    amount = VALUES(amount),
                    status = VALUES(status),
                    paid_at = VALUES(paid_at),
                    updated_at = VALUES(updated_at)
                """, (
                    row['id'],
                    row['company_id'],
                    row['amount'],
                    row['status'],
                    row['created_at'],
                    paid_at,
                    datetime.now()
                ))
            
            conexion.commit()
            print("Finalizado todo bien")
            
    except Error as e:
        print("Error MySQL:", e)
        if conexion and conexion.is_connected():
            conexion.rollback()
    except Exception as e:
        print("Error inesperado:", e)
    finally:
        if conexion and conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")

if __name__ == "__main__":
    cargarDatos()