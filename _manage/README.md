# _manage/ Directory

This directory contains the modular management system for all Data Engineering tools.

## Structure

### Tool Handlers
Each tool has its own handler module that manages setup, lifecycle, and configuration:
- `_kafka.py` - Apache Kafka (KRaft mode)
- `_kafka_zookeeper.py` - Apache Kafka with ZooKeeper
- `_spark.py` - Apache Spark
- `_hadoop.py` - Apache Hadoop
- `_airflow.py` - Apache Airflow
- `_flink.py` - Apache Flink

### Utilities
- `_base.py` - Base class for all tool handlers (common operations)
- `_docker_utils.py` - Docker operations and health checks
- `_system_check.py` - System dependency verification
- `_clean_all.py` - Complete cleanup script

## When to Edit Manually

**You typically DON'T need to edit these files manually.** The manager script handles everything automatically.

### Scenarios Where Manual Editing May Be Needed:

1. **Custom Docker Configurations**
   - If you need to modify Docker Compose settings (ports, volumes, environment variables)
   - Edit the `_tool_specific_setup()` method in the respective handler file

2. **Adding New Tools**
   - Create a new handler file following the pattern in existing handlers
   - Inherit from `ToolHandler` base class
   - Implement required methods: `get_subdirectories()`, `_tool_specific_setup()`

3. **Custom Health Checks**
   - Override `_wait_for_health()` method in the tool handler
   - Add custom URL checks or service-specific validation

4. **Port Conflicts**
   - Modify the `ports` dictionary in the handler's `__init__` method
   - Update the Docker Compose configuration accordingly

5. **Resource Limits**
   - Edit Docker Compose configurations in `_tool_specific_setup()` to add memory/CPU limits

## Best Practices

- **Don't modify `_base.py`** unless adding features for ALL tools
- **Test changes** using `python manager.py setup <tool>` before committing
- **Keep Docker Compose configs** in the handler files for maintainability
- **Use the cleanup script** (`_clean_all.py`) to reset environments during testing

## Troubleshooting

If a tool fails to start:
1. Check Docker is running: `docker info`
2. Check port availability: `python manager.py check-system`
3. View logs: `docker-compose -f <tool>/docker-compose.yml logs`
4. Clean and retry: `python manager.py cleanup <tool> && python manager.py setup <tool>`

## Development Workflow

1. Make changes to handler files
2. Test with: `python manager.py setup <tool>`
3. Verify with: `python manager.py start <tool>`
4. Check status: `python manager.py status <tool>`
5. Clean up: `python manager.py cleanup <tool>`
