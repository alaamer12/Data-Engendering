# Apache Airflow Practice Guide

## Overview

Apache Airflow is a platform to programmatically author, schedule, and monitor workflows.

## Access Information

After running `python manager.py start airflow`:
- **Webserver**: http://localhost:8085
- **Username**: `airflow`
- **Password**: `airflow`
- **Flower (Celery Monitor)**: http://localhost:5555

## Quick Start

```bash
# Setup and start (takes ~2 minutes)
python manager.py setup airflow
python manager.py start airflow

# Wait for services to initialize
# Access UI at http://localhost:8085
```

## Practice Exercises

### Exercise 1: Simple DAG

Create `dags/hello_world_dag.py`:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def print_hello():
    print("Hello from Airflow!")
    return "Success"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'hello_world',
    default_args=default_args,
    description='A simple hello world DAG',
    schedule_interval=timedelta(days=1),
    catchup=False
)

task = PythonOperator(
    task_id='print_hello',
    python_callable=print_hello,
    dag=dag
)
```

### Exercise 2: Task Dependencies

Create `dags/etl_dag.py`:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract():
    print("Extracting data...")
    return {"data": [1, 2, 3, 4, 5]}

def transform(**context):
    data = context['task_instance'].xcom_pull(task_ids='extract')
    print(f"Transforming {data}")
    return {"transformed": [x * 2 for x in data['data']]}

def load(**context):
    data = context['task_instance'].xcom_pull(task_ids='transform')
    print(f"Loading {data}")

with DAG(
    'etl_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract
    )
    
    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform
    )
    
    load_task = PythonOperator(
        task_id='load',
        python_callable=load
    )
    
    extract_task >> transform_task >> load_task
```

### Exercise 3: Branching

```python
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime

def decide_branch(**context):
    hour = datetime.now().hour
    if hour < 12:
        return 'morning_task'
    else:
        return 'afternoon_task'

def morning():
    print("Good morning!")

def afternoon():
    print("Good afternoon!")

with DAG('branching_dag', start_date=datetime(2024, 1, 1), schedule_interval='@hourly', catchup=False) as dag:
    branch = BranchPythonOperator(
        task_id='branch',
        python_callable=decide_branch
    )
    
    morning_task = PythonOperator(task_id='morning_task', python_callable=morning)
    afternoon_task = PythonOperator(task_id='afternoon_task', python_callable=afternoon)
    
    branch >> [morning_task, afternoon_task]
```

### Exercise 4: Sensors

```python
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from datetime import datetime

def process_file():
    print("Processing file...")

with DAG('sensor_dag', start_date=datetime(2024, 1, 1), schedule_interval='@daily', catchup=False) as dag:
    wait_for_file = FileSensor(
        task_id='wait_for_file',
        filepath='/opt/airflow/data/input.txt',
        poke_interval=10,
        timeout=300
    )
    
    process = PythonOperator(
        task_id='process',
        python_callable=process_file
    )
    
    wait_for_file >> process
```

## Project Ideas

1. **Data Pipeline**: Daily ETL from API to database
2. **Report Generator**: Scheduled reports with email notifications
3. **ML Pipeline**: Train and deploy models on schedule
4. **Data Quality**: Automated data validation workflows

## Key Concepts

- **DAG**: Directed Acyclic Graph of tasks
- **Operators**: Units of work (Python, Bash, SQL, etc.)
- **Tasks**: Instances of operators
- **XComs**: Cross-communication between tasks
- **Sensors**: Wait for conditions
- **Hooks**: Connections to external systems

## Monitoring

- **DAG View**: Visualize task dependencies
- **Tree View**: See historical runs
- **Graph View**: Current DAG structure
- **Gantt Chart**: Task duration analysis
- **Logs**: Debug task failures

## Troubleshooting

```bash
# View logs
docker-compose -f airflow/docker-compose.yml logs -f airflow-webserver

# List DAGs
docker exec -it airflow-webserver airflow dags list

# Test a task
docker exec -it airflow-webserver airflow tasks test hello_world print_hello 2024-01-01

# Trigger DAG manually
docker exec -it airflow-webserver airflow dags trigger hello_world
```

## Resources

- [Airflow Documentation](https://airflow.apache.org/docs/)
- [DAG Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Operators Guide](https://airflow.apache.org/docs/apache-airflow/stable/operators-and-hooks-ref.html)
