from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def hola_mundo():
    print("¡Hola Mundo desde Airflow!")
    return "Ejecución exitosa"

def procesar_datos():
    import pandas as pd
    
    data = {
        'nombre': ['Juan', 'María', 'Pedro', 'Laura'],
        'edad': [25, 30, 35, 28],
        'ciudad': ['Buenos Aires', 'Córdoba', 'Mendoza', 'Rosario']
    }
    
    df = pd.DataFrame(data)
    print("DataFrame creado:")
    print(df)
    return df.to_dict()

with DAG(
    'hola_mundo_simple',
    default_args=default_args,
    description='DAG simple sin timezone complejo',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['ejemplo'],
) as dag:

    inicio = DummyOperator(task_id='inicio')
    tarea_hola = PythonOperator(task_id='hola_mundo', python_callable=hola_mundo)
    tarea_datos = PythonOperator(task_id='procesar_datos', python_callable=procesar_datos)
    fin = DummyOperator(task_id='fin')

    inicio >> tarea_hola >> tarea_datos >> fin