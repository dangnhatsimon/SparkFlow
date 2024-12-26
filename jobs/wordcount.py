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