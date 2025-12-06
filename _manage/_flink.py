"""
Apache Flink handler.
"""

from pathlib import Path
from _manage._base import ToolHandler


class FlinkHandler(ToolHandler):
    def __init__(self, base_dir: str):
        super().__init__(
            tool_name="Flink",
            tool_dir=Path(base_dir) / "flink",
            ports={
                "Flink JobManager UI": 8086
            }
        )
    
    def get_subdirectories(self):
        return ["exercises", "data", "logs", "checkpoints", "savepoints"]
    
    def _tool_specific_setup(self) -> bool:
        """Create Flink docker-compose.yml"""
        docker_compose_content = """version: '3.8'

services:
  jobmanager:
    image: flink:1.19.0
    container_name: flink-jobmanager
    ports:
      - "8086:8081"
    command: jobmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager
    volumes:
      - ./data:/data
      - ./logs:/opt/flink/log
      - ./checkpoints:/checkpoints
      - ./savepoints:/savepoints
      - ./exercises:/opt/flink/jobs
    networks:
      - flink-network

  taskmanager-1:
    image: flink:1.19.0
    container_name: flink-taskmanager-1
    depends_on:
      - jobmanager
    command: taskmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager
      - TASK_MANAGER_NUMBER_OF_TASK_SLOTS=2
    volumes:
      - ./data:/data
      - ./logs:/opt/flink/log
      - ./checkpoints:/checkpoints
      - ./savepoints:/savepoints
    networks:
      - flink-network

  taskmanager-2:
    image: flink:1.19.0
    container_name: flink-taskmanager-2
    depends_on:
      - jobmanager
    command: taskmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager
      - TASK_MANAGER_NUMBER_OF_TASK_SLOTS=2
    volumes:
      - ./data:/data
      - ./logs:/opt/flink/log
      - ./checkpoints:/checkpoints
      - ./savepoints:/savepoints
    networks:
      - flink-network

networks:
  flink-network:
    driver: bridge
"""
        
        with open(self.docker_compose_file, 'w') as f:
            f.write(docker_compose_content)
        
        return True
    
    def _wait_for_health(self) -> bool:
        """Wait for Flink to be ready"""
        from _manage._docker_utils import wait_for_url
        import time
        
        time.sleep(10)
        return wait_for_url("http://localhost:8086", timeout=60)
