"""
Apache Spark handler.
"""

from pathlib import Path
from _manage._base import ToolHandler


class SparkHandler(ToolHandler):
    def __init__(self, base_dir: str):
        super().__init__(
            tool_name="Spark",
            tool_dir=Path(base_dir) / "spark",
            ports={
                "Spark Master UI": 8082,
                "Spark Worker 1 UI": 8083,
                "Spark Worker 2 UI": 8084,
                "Jupyter Notebook": 8888
            }
        )
    
    def get_subdirectories(self):
        return ["exercises", "data", "logs", "notebooks"]
    
    def _tool_specific_setup(self) -> bool:
        """Create Spark docker-compose.yml"""
        docker_compose_content = """version: '3.8'

services:
  spark-master:
    image: bitnami/spark:3.5.7
    container_name: spark-master
    ports:
      - "8082:8080"
      - "7077:7077"
    environment:
      - SPARK_MODE=master
      - SPARK_RPC_AUTHENTICATION_ENABLED=no
      - SPARK_RPC_ENCRYPTION_ENABLED=no
      - SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no
      - SPARK_SSL_ENABLED=no
    volumes:
      - ./data:/opt/spark-data
      - ./logs:/opt/spark/logs
      - ./exercises:/opt/spark-apps
    networks:
      - spark-network

  spark-worker-1:
    image: bitnami/spark:3.5.7
    container_name: spark-worker-1
    ports:
      - "8083:8081"
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
      - SPARK_WORKER_MEMORY=2G
      - SPARK_WORKER_CORES=2
      - SPARK_RPC_AUTHENTICATION_ENABLED=no
      - SPARK_RPC_ENCRYPTION_ENABLED=no
      - SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no
      - SPARK_SSL_ENABLED=no
    volumes:
      - ./data:/opt/spark-data
      - ./logs:/opt/spark/logs
    depends_on:
      - spark-master
    networks:
      - spark-network

  spark-worker-2:
    image: bitnami/spark:3.5.7
    container_name: spark-worker-2
    ports:
      - "8084:8081"
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
      - SPARK_WORKER_MEMORY=2G
      - SPARK_WORKER_CORES=2
      - SPARK_RPC_AUTHENTICATION_ENABLED=no
      - SPARK_RPC_ENCRYPTION_ENABLED=no
      - SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no
      - SPARK_SSL_ENABLED=no
    volumes:
      - ./data:/opt/spark-data
      - ./logs:/opt/spark/logs
    depends_on:
      - spark-master
    networks:
      - spark-network

  jupyter:
    image: jupyter/pyspark-notebook:latest
    container_name: spark-jupyter
    ports:
      - "8888:8888"
    environment:
      - JUPYTER_ENABLE_LAB=yes
      - SPARK_MASTER=spark://spark-master:7077
    volumes:
      - ./notebooks:/home/jovyan/work
      - ./data:/home/jovyan/data
    depends_on:
      - spark-master
    networks:
      - spark-network

networks:
  spark-network:
    driver: bridge
"""
        
        with open(self.docker_compose_file, 'w') as f:
            f.write(docker_compose_content)
        
        return True
    
    def _wait_for_health(self) -> bool:
        """Wait for Spark to be ready"""
        from _manage._docker_utils import wait_for_url
        import time
        
        time.sleep(10)
        return wait_for_url("http://localhost:8082", timeout=60)
