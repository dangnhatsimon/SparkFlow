from __future__ import annotations
import pendulum
from airflow.decorators import dag, task
from airflow.utils import *
from airflow.models import Variable
from airflow.models import DagRun
from airflow.models.taskinstance import TaskInstance
from airflow.utils.state import State
from airflow.utils.trigger_rule import TriggerRule
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from datetime import datetime, timedelta
import json
from airflow.models.baseoperator import chain
from pyspark import SparkContext
from pyspark.sql import SparkSession
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
import pandas as pd


# @task.pyspark(conn_id="spark-conn")
# def read_data(spark: SparkSession, sc: SparkContext):
#     df = spark.createDataFrame(
#         [
#             (1, "John Doe", 21),
#             (2, "Jane Doe", 22),
#             (3, "Joe Bloggs", 23),
#         ],
#         ["id", "name", "age"],
#     )
#     df.show()

#     return df.toPandas()


@dag(
    dag_id="spark_airflow",
    start_date=pendulum.datetime(2024, 6, 1, tz="Asia/Ho_Chi_Minh"),
    schedule="0 22 * * SUN",
    catchup=False,
    tags=["spark", "airflow", "nhat.d"]
)
def spark_airflow():
    python_job = SparkSubmitOperator(
        task_id="python_job",
        application="jobs/wordcount.py",
        conn_id="spark-conn",
        total_executor_cores="4",
        executor_cores="2",
        executor_memory="1g",
        num_executors="2",
        driver_memory="2g",
        verbose=False
    )


spark_airflow()
