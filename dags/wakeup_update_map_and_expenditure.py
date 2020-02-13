from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'HiGeorge',
    'depends_on_past': False,
    'start_date': datetime(2020, 2, 4),
    'email': ['<HG_email_address>'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('wakeup', default_args=default_args, schedule_interval=timedelta(minutes=1))

t = BashOperator(
    task_id='wake_up',
    bash_command='<python3 address of act_on_active_campaigns.py>',
    dag=dag)