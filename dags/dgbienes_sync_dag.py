from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Configuración del DAG
default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definir el DAG
with DAG(
    'dgbienes_sync',
    default_args=default_args,
    description='Sincronización DGBienes a SQL Server',
    schedule_interval='0 10 * * *',
    catchup=False,
    tags=['dgbienes', 'sync', 'sqlserver'],
    max_active_runs=1,
) as dag:

    # Comando simple ejecutando desde el volumen montado
    sync_command = '''
    cd /opt/airflow/dgbienes && \
    export APP_ENV=bienes && \
    python main.py --mode sqlserver --sync-mode incremental
    '''

    sync_task = BashOperator(
        task_id='sync_dgbienes_to_sqlserver',
        bash_command=sync_command,
        execution_timeout=timedelta(hours=2),
        env={'APP_ENV': 'bienes'}
    )

    # Verificar estado
    status_command = '''
    cd /opt/airflow/dgbienes && \
    export APP_ENV=bienes && \
    python main.py --status
    '''

    status_task = BashOperator(
        task_id='check_sync_status',
        bash_command=status_command,
        trigger_rule='all_success',
        env={'APP_ENV': 'bienes'}
    )

    sync_task >> status_task