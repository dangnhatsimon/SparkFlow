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
from airflow.operators.bash import BashOperator


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
    spark_wordcount = SparkSubmitOperator(
        name="spark_wordcount",
        task_id="spark_wordcount",
        application="./jobs/wordcount.py",
        conn_id="spark_connection",
        # conf={"spark.master": "spark://172.19.0.3:7077"},
        total_executor_cores=4,
        executor_cores=2,
        executor_memory="1G",
        num_executors=2,
        driver_memory="2G",
        verbose=False,
        deploy_mode="client",
        spark_binary="spark-submit"
    )
    # airflow connections add 'spark_connection' --conn-type 'spark' --conn-host 'spark://sparkflow-spark-master-1:9090'
    # airflow connections add 'spark_connection' --conn-type 'spark' --conn-host 'spark://sparkflow-spark-master-1:8080'

    spark_wordcount_bash = BashOperator(
        task_id="spark_wordcount_bash",
        bash_command="docker exec sparkflow-spark-master-1 spark-submit --master spark://sparkflow-spark-master-1:7077 --num-executors 2 --total-executor-cores 4 --executor-cores 2 --executor-memory 1g --driver-memory 2g --name arrow-spark --deploy-mode client ./jobs/wordcount.py"
    )


spark_airflow()
