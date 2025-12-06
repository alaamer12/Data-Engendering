"""
Apache Hadoop handler.
"""

from pathlib import Path
from _manage._base import ToolHandler


class HadoopHandler(ToolHandler):
    def __init__(self, base_dir: str):
        super().__init__(
            tool_name="Hadoop",
            tool_dir=Path(base_dir) / "hadoop",
            ports={
                "NameNode UI": 9870,
                "DataNode UI": 9864,
                "ResourceManager UI": 8088,
                "NodeManager UI": 8042
            }
        )
    
    def get_subdirectories(self):
        return ["exercises", "data", "logs", "namenode", "datanode"]
    
    def _tool_specific_setup(self) -> bool:
        """Create Hadoop docker-compose.yml"""
        docker_compose_content = """version: '3.8'

services:
  namenode:
    image: bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8
    container_name: hadoop-namenode
    ports:
      - "9870:9870"
      - "9000:9000"
    environment:
      - CLUSTER_NAME=hadoop-cluster
      - CORE_CONF_fs_defaultFS=hdfs://namenode:9000
    volumes:
      - ./namenode:/hadoop/dfs/name
      - ./data:/data
    networks:
      - hadoop-network

  datanode:
    image: bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8
    container_name: hadoop-datanode
    ports:
      - "9864:9864"
    environment:
      - CORE_CONF_fs_defaultFS=hdfs://namenode:9000
      - SERVICE_PRECONDITION=namenode:9870
    volumes:
      - ./datanode:/hadoop/dfs/data
    depends_on:
      - namenode
    networks:
      - hadoop-network

  resourcemanager:
    image: bde2020/hadoop-resourcemanager:2.0.0-hadoop3.2.1-java8
    container_name: hadoop-resourcemanager
    ports:
      - "8088:8088"
    environment:
      - CORE_CONF_fs_defaultFS=hdfs://namenode:9000
      - YARN_CONF_yarn_resourcemanager_hostname=resourcemanager
      - SERVICE_PRECONDITION=namenode:9000 namenode:9870 datanode:9864
    depends_on:
      - namenode
      - datanode
    networks:
      - hadoop-network

  nodemanager:
    image: bde2020/hadoop-nodemanager:2.0.0-hadoop3.2.1-java8
    container_name: hadoop-nodemanager
    ports:
      - "8042:8042"
    environment:
      - CORE_CONF_fs_defaultFS=hdfs://namenode:9000
      - YARN_CONF_yarn_resourcemanager_hostname=resourcemanager
      - SERVICE_PRECONDITION=namenode:9000 namenode:9870 datanode:9864 resourcemanager:8088
    depends_on:
      - namenode
      - datanode
      - resourcemanager
    networks:
      - hadoop-network

networks:
  hadoop-network:
    driver: bridge
"""
        
        with open(self.docker_compose_file, 'w') as f:
            f.write(docker_compose_content)
        
        return True
    
    def _wait_for_health(self) -> bool:
        """Wait for Hadoop to be ready"""
        from _manage._docker_utils import wait_for_url
        import time
        
        time.sleep(20)
        return wait_for_url("http://localhost:9870", timeout=90)
