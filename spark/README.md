# Apache Spark Practice Guide

## Overview

Apache Spark is a unified analytics engine for large-scale data processing. This setup includes a master node, 2 worker nodes, and Jupyter notebook integration.

## Access Information

After running `python manager.py start spark`:
- **Spark Master UI**: http://localhost:8082
- **Worker 1 UI**: http://localhost:8083
- **Worker 2 UI**: http://localhost:8084
- **Jupyter Notebook**: http://localhost:8888 (check logs for token)

## Quick Start

```bash
# Setup and start
python manager.py setup spark
python manager.py start spark

# Get Jupyter token
docker logs spark-jupyter | grep token
```

## Practice Exercises

### Exercise 1: PySpark Shell

```bash
# Enter Spark master container
docker exec -it spark-master bash

# Start PySpark shell
pyspark --master spark://spark-master:7077
```

```python
# Create RDD
data = [1, 2, 3, 4, 5]
rdd = sc.parallelize(data)

# Transformations
squared = rdd.map(lambda x: x ** 2)
filtered = squared.filter(lambda x: x > 10)

# Action
result = filtered.collect()
print(result)  # [16, 25]
```

### Exercise 2: DataFrame Operations

Create `exercises/dataframe_basics.py`:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("DataFrame Basics") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Create DataFrame
data = [
    ("Alice", 25, "Engineer"),
    ("Bob", 30, "Manager"),
    ("Charlie", 35, "Director")
]
df = spark.createDataFrame(data, ["name", "age", "role"])

# Show DataFrame
df.show()

# Select columns
df.select("name", "age").show()

# Filter
df.filter(df.age > 28).show()

# Group and aggregate
df.groupBy("role").count().show()

spark.stop()
```

### Exercise 3: Spark SQL

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SQL Example").getOrCreate()

# Create temp view
df.createOrReplaceTempView("employees")

# SQL queries
result = spark.sql("""
    SELECT role, AVG(age) as avg_age
    FROM employees
    GROUP BY role
    ORDER BY avg_age DESC
""")

result.show()
```

### Exercise 4: Reading/Writing Data

```python
# Read CSV
df = spark.read.csv("/opt/spark-data/sample.csv", header=True, inferSchema=True)

# Write Parquet
df.write.parquet("/opt/spark-data/output.parquet", mode="overwrite")

# Read Parquet
parquet_df = spark.read.parquet("/opt/spark-data/output.parquet")
```

### Exercise 5: Jupyter Notebook

1. Access Jupyter at http://localhost:8888
2. Create a new notebook
3. Run Spark code interactively:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Jupyter Example") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Your Spark code here
df = spark.range(1000)
df.show()
```

## Project Ideas

1. **Sales Analysis**: Analyze e-commerce sales data with aggregations
2. **Log Processing**: Parse and analyze web server logs
3. **ETL Pipeline**: Extract, transform, and load data between formats
4. **Machine Learning**: Use MLlib for classification/regression

## Key Concepts

- **RDD**: Resilient Distributed Dataset (low-level API)
- **DataFrame**: Structured data with schema (high-level API)
- **Transformations**: Lazy operations (map, filter, join)
- **Actions**: Trigger computation (collect, count, save)
- **DAG**: Directed Acyclic Graph of operations
- **Partitions**: Data distribution across workers

## Monitoring

- **Master UI** (http://localhost:8082): View applications, workers, resources
- **Worker UIs**: Monitor tasks and executors
- **Application UI**: Track job progress and stages

## Troubleshooting

```bash
# View logs
docker-compose -f spark/docker-compose.yml logs -f spark-master

# Check worker connection
# Should see 2 workers in Master UI

# Submit a job
docker exec -it spark-master spark-submit \
    --master spark://spark-master:7077 \
    /opt/spark-apps/your_script.py
```

## Resources

- [Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
