from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def debug_test():
    print("=== DEBUG TEST ===")
    print("1. Funcion básica OK")
    
    # Test imports
    try:
        import pendulum
        print("2. Pendulum OK")
    except ImportError as e:
        print("2. Pendulum ERROR:", e)
    
    try:
        import pandas
        print("3. Pandas OK")
    except ImportError as e:
        print("3. Pandas ERROR:", e)
    
    print("4. Finalizado")
    return "Debug completado"

with DAG(
    'debug_simple_dag',
    description='DAG para debug',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['debug'],
) as dag:

    debug_task = PythonOperator(
        task_id='debug_test',
        python_callable=debug_test,
    )