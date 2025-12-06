# Apache Flink Practice Guide

## Overview

Apache Flink is a stream processing framework for real-time analytics.

## Access Information

After running `python manager.py start flink`:
- **JobManager UI**: http://localhost:8086

## Quick Start

```bash
python manager.py setup flink
python manager.py start flink
```

## Practice Exercises

### Exercise 1: Word Count (Streaming)

Create `exercises/word_count.py`:

```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(env)

# Create source table
t_env.execute_sql("""
    CREATE TABLE words (
        word STRING
    ) WITH (
        'connector' = 'datagen',
        'rows-per-second' = '10'
    )
""")

# Create sink table
t_env.execute_sql("""
    CREATE TABLE word_count (
        word STRING,
        cnt BIGINT
    ) WITH (
        'connector' = 'print'
    )
""")

# Execute query
t_env.execute_sql("""
    INSERT INTO word_count
    SELECT word, COUNT(*) as cnt
    FROM words
    GROUP BY word
""")
```

### Exercise 2: Windowing

```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import Types
from pyflink.datastream.window import TumblingProcessingTimeWindows
from pyflink.common.time import Time

env = StreamExecutionEnvironment.get_execution_environment()

# Create stream
ds = env.from_collection(
    collection=[(1, 'a'), (2, 'b'), (3, 'a'), (4, 'c')],
    type_info=Types.TUPLE([Types.INT(), Types.STRING()])
)

# Apply window
windowed = ds.key_by(lambda x: x[1]) \
    .window(TumblingProcessingTimeWindows.of(Time.seconds(5))) \
    .reduce(lambda a, b: (a[0] + b[0], a[1]))

windowed.print()
env.execute("Windowing Example")
```

## Key Concepts

- **DataStream API**: Core streaming abstraction
- **Windows**: Time-based or count-based grouping
- **State**: Managed state for stateful operations
- **Checkpoints**: Fault tolerance mechanism
- **Event Time**: Processing based on event timestamps

## Resources

- [Flink Documentation](https://flink.apache.org/docs/)
- [PyFlink Guide](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/python/)
