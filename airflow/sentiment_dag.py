from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import subprocess
import pandas as pd
from sqlalchemy import create_engine
import os

default_args = {
    'owner': 'ranjith',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'sentiment_analysis_pipeline',
    default_args=default_args,
    description='Social Media Sentiment Analysis Pipeline',
    schedule_interval='@daily',
    start_date=datetime(2026, 4, 22),
    catchup=False
)

def extract_and_load():
    os.environ['PATH'] = '/opt/hd/bin:/opt/hd/sbin:' + os.environ['PATH']
    engine = create_engine('mysql+pymysql://root:YOUR_PASSWORD@localhost/sentiment_db')
    posts_df = pd.read_sql("SELECT * FROM social_posts", engine)
    posts_df.to_csv('/tmp/social_posts.csv', index=False)
    subprocess.run(["hdfs", "dfs", "-mkdir", "-p", "/sentiment/raw_posts"])
    subprocess.run(["hdfs", "dfs", "-put", "-f", "/tmp/social_posts.csv", "/sentiment/raw_posts/"])
    print("ETL Complete!")

task1 = PythonOperator(
    task_id='extract_load_to_hdfs',
    python_callable=extract_and_load,
    dag=dag
)

task2 = BashOperator(
    task_id='run_spark_sentiment_analysis',
    bash_command='source ~/.bashrc && spark-submit ~/projects/sentiment_analysis/pyspark/analyze_sentiment.py',
    dag=dag
)

task3 = BashOperator(
    task_id='query_hive_results',
    bash_command='hive -e "USE sentiment_dw; SELECT sentiment, COUNT(*) FROM sentiment_analysis GROUP BY sentiment;"',
    dag=dag
)

task1 >> task2 >> task3
