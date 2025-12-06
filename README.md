# Data Engineering Practice Environment

A comprehensive, Docker-based practice environment for learning and mastering Data Engineering tools. Manage Kafka, Spark, Hadoop, Airflow, and Flink with a single unified CLI.

## 🚀 Quick Start

### Prerequisites

- **Docker** (Docker Desktop for Windows or Docker in GitHub Codespaces)
- **Python 3.8+**
- **10+ GB free disk space**

### Installation

```bash
# Clone or navigate to the DE directory
cd C:\Users\amrmu\Downloads\DE  # or your path

# Install Python dependencies
python -m pip install -r requirements.txt

# Check system requirements
python manager.py check-system
```

### Basic Usage

```bash
# List available tools
python manager.py list

# Setup a tool (creates directories and configurations)
python manager.py setup kafka

# Start the tool
python manager.py start kafka

# Check status
python manager.py status kafka

# Stop the tool
python manager.py stop kafka

# Clean up (remove containers and volumes)
python manager.py cleanup kafka
```

## 📦 Available Tools

| Tool | Description | Ports |
|------|-------------|-------|
| **kafka** | Apache Kafka (KRaft mode) | 9092 (Broker), 8080 (UI) |
| **kafka_zookeeper** | Kafka with ZooKeeper | 9093 (Broker), 2181 (ZK), 8081 (UI) |
| **spark** | Apache Spark cluster | 8082 (Master), 8888 (Jupyter) |
| **hadoop** | Hadoop HDFS + YARN | 9870 (NameNode), 8088 (YARN) |
| **airflow** | Workflow orchestration | 8085 (Webserver), 5555 (Flower) |
| **flink** | Stream processing | 8086 (JobManager) |

## 🎯 Learning Path

See [LEARNING_ROADMAP.md](LEARNING_ROADMAP.md) for a comprehensive learning guide.

### Beginner Track
1. Start with **Kafka** - Learn message streaming basics
2. Move to **Spark** - Process data with distributed computing
3. Try **Airflow** - Orchestrate data pipelines

### Advanced Track
4. **Hadoop** - Understand HDFS and MapReduce
5. **Flink** - Real-time stream processing
6. **Integration Projects** - Combine multiple tools

## 📖 Tool-Specific Guides

Each tool has its own directory with:
- `README.md` - Tool-specific documentation and exercises
- `docker-compose.yml` - Service configuration
- `exercises/` - Practice scripts and examples
- `data/` - Sample datasets
- `logs/` - Application logs

### Example: Kafka Practice

```bash
# Setup and start Kafka
python manager.py setup kafka
python manager.py start kafka

# Access Kafka UI at http://localhost:8080
# Follow exercises in kafka/README.md
```

## 🛠️ Advanced Usage

### Clean Up All Tools

```bash
# Interactive cleanup (removes all containers and volumes)
python manager.py clean-all

# Or use the cleanup script directly
python _manage/_clean_all.py

# Dry run (see what would be cleaned)
python _manage/_clean_all.py --dry-run

# Remove data directories too
python _manage/_clean_all.py --remove-data
```

### System Health Check

```bash
python manager.py check-system
```

This checks:
- Docker daemon status
- Docker Compose installation
- Python version
- Disk space
- Required Python packages

### Port Conflicts

If you encounter port conflicts, you can modify ports in the tool handler files:
- Edit `_manage/_<tool>.py`
- Update the `ports` dictionary in `__init__`
- Update the Docker Compose configuration in `_tool_specific_setup()`

## 🐛 Troubleshooting

### Docker Not Running

```bash
# Windows: Start Docker Desktop
# Codespaces: Docker should be pre-installed

# Verify Docker is running
docker info
```

### Port Already in Use

```bash
# Check what's using the port
netstat -ano | findstr :8080  # Windows
lsof -i :8080                 # Linux/Mac

# Stop the conflicting service or use cleanup
python manager.py cleanup <tool>
```

### Services Not Starting

```bash
# View logs
cd <tool-directory>
docker-compose logs

# Clean and retry
python manager.py cleanup <tool>
python manager.py setup <tool>
python manager.py start <tool>
```

### Python Package Issues

```bash
# Reinstall dependencies
python -m pip install -r requirements.txt --force-reinstall

# Use virtual environment (recommended)
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## 📁 Project Structure

```
DE/
├── manager.py              # Main CLI entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LEARNING_ROADMAP.md    # Learning guide
│
├── _manage/               # Management modules (don't edit unless necessary)
│   ├── README.md          # Internal documentation
│   ├── _base.py           # Base handler class
│   ├── _docker_utils.py   # Docker utilities
│   ├── _system_check.py   # System checks
│   ├── _clean_all.py      # Cleanup script
│   ├── _kafka.py          # Kafka handler
│   ├── _kafka_zookeeper.py
│   ├── _spark.py
│   ├── _hadoop.py
│   ├── _airflow.py
│   └── _flink.py
│
├── kafka/                 # Kafka (KRaft) environment
│   ├── README.md
│   ├── docker-compose.yml
│   ├── exercises/
│   ├── data/
│   └── logs/
│
├── kafka_zookeeper/       # Kafka with ZooKeeper
├── spark/                 # Spark environment
├── hadoop/                # Hadoop environment
├── airflow/               # Airflow environment
└── flink/                 # Flink environment
```

## 🎓 Practice Exercises

Each tool directory contains practice exercises:

- **kafka/exercises/** - Producer/Consumer patterns, topic management
- **spark/exercises/** - RDD operations, DataFrame API, Spark SQL
- **hadoop/exercises/** - HDFS operations, MapReduce jobs
- **airflow/dags/** - DAG examples, operators, scheduling
- **flink/exercises/** - Stream processing, windowing, state management

## 🌟 Best Practices

1. **Use Virtual Environments** - Isolate Python dependencies
2. **Start One Tool at a Time** - Avoid resource conflicts
3. **Check System Requirements** - Run `check-system` before starting
4. **Clean Up Regularly** - Use `cleanup` to free resources
5. **Read Tool READMEs** - Each tool has specific usage patterns
6. **Monitor Resources** - Use `docker stats` to check resource usage

## 🔗 Useful Commands

```bash
# View all running containers
docker ps

# View resource usage
docker stats

# View logs for a specific service
docker-compose -f kafka/docker-compose.yml logs -f

# Execute commands in a container
docker exec -it kafka-kraft bash

# Remove all stopped containers
docker container prune
```

## 📚 Additional Resources

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Apache Hadoop Documentation](https://hadoop.apache.org/docs/current/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Apache Flink Documentation](https://flink.apache.org/docs/)

## 🤝 Contributing

This is a personal practice environment. Feel free to:
- Add new tools by creating handlers in `_manage/`
- Enhance exercises in tool directories
- Improve documentation

## 📝 License

This project is for educational purposes.

---

**Happy Learning! 🚀**

For detailed learning paths and project ideas, see [LEARNING_ROADMAP.md](LEARNING_ROADMAP.md)
