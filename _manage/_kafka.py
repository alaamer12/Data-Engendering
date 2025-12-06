"""
Apache Kafka (KRaft mode) handler.
"""

from pathlib import Path
from _manage._base import ToolHandler


class KafkaHandler(ToolHandler):
    def __init__(self, base_dir: str):
        super().__init__(
            tool_name="Kafka (KRaft)",
            tool_dir=Path(base_dir) / "kafka",
            ports={
                "Kafka Broker": 9092,
                "Kafka UI": 8080
            }
        )
    
    def get_subdirectories(self):
        return ["exercises", "data", "logs", "config"]
    
    def _tool_specific_setup(self) -> bool:
        """Create Kafka-specific docker-compose.yml"""
        # Note: CLUSTER_ID should be a base64-encoded UUID
        # Generated using: kafka-storage random-uuid
        # For simplicity, using a valid pre-generated ID
        # In production, generate unique ID per cluster
        docker_compose_content = """version: '3.8'

services:
  kafka:
    image: apache/kafka:3.8.1
    container_name: kafka-kraft
    ports:
      - "9092:9092"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_NUM_PARTITIONS: 3
      CLUSTER_ID: MkU3OEVBNTcwNTJENDM2Qk
    volumes:
      - ./data:/var/lib/kafka/data
      - ./logs:/var/log/kafka
    networks:
      - kafka-network

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    container_name: kafka-ui
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9092
      DYNAMIC_CONFIG_ENABLED: 'true'
    depends_on:
      - kafka
    networks:
      - kafka-network

networks:
  kafka-network:
    driver: bridge
"""
        
        with open(self.docker_compose_file, 'w') as f:
            f.write(docker_compose_content)
        
        return True
    
    def _wait_for_health(self) -> bool:
        """Wait for Kafka to be ready"""
        from _manage._docker_utils import wait_for_url
        import time
        
        # Wait a bit for Kafka to initialize
        time.sleep(10)
        
        # Check if Kafka UI is accessible
        return wait_for_url("http://localhost:8080", timeout=60)
