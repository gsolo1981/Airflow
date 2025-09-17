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
    'dgbienes_multi_env_sync',
    default_args=default_args,
    description='Sincronización DGBienes - Bienes y Concesiones',
    schedule_interval='0 2 * * *',
    catchup=False,
    tags=['dgbienes', 'sync', 'multi-env'],
    max_active_runs=1,
) as dag:

    # ========== BIENES ==========
    sync_bienes = BashOperator(
        task_id='sync_bienes_to_sqlserver',
        bash_command='''
        cd /opt/airflow/dgbienes && \
        export APP_ENV=bienes && \
        python main.py --mode sqlserver --sync-mode incremental
        ''',
        execution_timeout=timedelta(hours=2),
        env={'APP_ENV': 'bienes'}
    )

    status_bienes = BashOperator(
        task_id='check_bienes_status',
        bash_command='''
        cd /opt/airflow/dgbienes && \
        export APP_ENV=bienes && \
        python main.py --status
        ''',
        trigger_rule='all_success',
        env={'APP_ENV': 'bienes'}
    )

    # ========== CONCESIONES ==========
    sync_concesiones = BashOperator(
        task_id='sync_concesiones_to_sqlserver',
        bash_command='''
        cd /opt/airflow/dgbienes && \
        export APP_ENV=concesiones && \
        python main.py --mode sqlserver --sync-mode incremental
        ''',
        execution_timeout=timedelta(hours=2),
        env={'APP_ENV': 'concesiones'}
    )

    status_concesiones = BashOperator(
        task_id='check_concesiones_status',
        bash_command='''
        cd /opt/airflow/dgbienes && \
        export APP_ENV=concesiones && \
        python main.py --status
        ''',
        trigger_rule='all_success',
        env={'APP_ENV': 'concesiones'}
    )

    # ========== DEPENDENCIAS ==========
    # Ejecutar en paralelo ambos entornos
    #sync_bienes >> status_bienes
    #sync_concesiones >> status_concesiones

    # Para ejecutar secuencial:
    sync_bienes >> status_bienes >> sync_concesiones >> status_concesiones