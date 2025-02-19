from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark import SparkContext

conf = SparkConf()
conf.setMaster("local[*]").setAppName("PythonWordCount")

sc = SparkContext.getOrCreate(conf=conf)

# spark = SparkSession.builder.appName("PythonWordCount").getOrCreate()

text = "Hello Spark Hello Python Hello Airflow Hello Docker Hello Nhat"

words = sc.parallelize(text.split(" "))

wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

for wc in wordCounts.collect():
    print(wc[0], wc[1])

sc.stop()


# docker exec -it e10494b92f36 spark-submit --master spark://172.19.0.3:7077 --num-executors 2 --total-executor-cores 4 --executor-cores 2 --executor-memory 1g --driver-memory 2g --name arrow-spark --deploy-mode client ./jobs/wordcount.py
# docker exec -it sparkflow-spark-master-1 spark-submit --master spark://172.19.0.3:7077 --num-executors 2 --total-executor-cores 4 --executor-cores 2 --executor-memory 1g --driver-memory 2g --name arrow-spark --deploy-mode client ./jobs/wordcount.py