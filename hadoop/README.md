# Apache Hadoop Practice Guide

## Overview

Apache Hadoop provides distributed storage (HDFS) and processing (MapReduce/YARN).

## Access Information

After running `python manager.py start hadoop`:
- **NameNode UI**: http://localhost:9870
- **DataNode UI**: http://localhost:9864
- **ResourceManager UI**: http://localhost:8088
- **NodeManager UI**: http://localhost:8042

## Quick Start

```bash
python manager.py setup hadoop
python manager.py start hadoop
```

## Practice Exercises

### Exercise 1: HDFS Commands

```bash
# Enter NameNode container
docker exec -it hadoop-namenode bash

# Create directory
hdfs dfs -mkdir -p /user/hadoop/input

# Upload file
hdfs dfs -put /data/sample.txt /user/hadoop/input/

# List files
hdfs dfs -ls /user/hadoop/input

# View file content
hdfs dfs -cat /user/hadoop/input/sample.txt

# Download file
hdfs dfs -get /user/hadoop/input/sample.txt ./local-copy.txt

# Delete file
hdfs dfs -rm /user/hadoop/input/sample.txt
```

### Exercise 2: HDFS Status

```bash
# Check HDFS health
hdfs dfsadmin -report

# Check file system
hdfs fsck /

# View block information
hdfs fsck /user/hadoop/input -files -blocks -locations
```

## Key Concepts

- **HDFS**: Distributed file system
- **NameNode**: Metadata management
- **DataNode**: Actual data storage
- **Replication**: Data redundancy (default: 3)
- **Blocks**: Data chunks (default: 128MB)

## Resources

- [Hadoop Documentation](https://hadoop.apache.org/docs/current/)
- [HDFS Architecture](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)
