# streaming-spark-stack

## Introduction & Learning Goals
This repository is my personal learning project where I practice building an end-to-end data engineering pipeline that demonstrates the flow of data from ingestion to streaming, processing, and finally storage, all within a containerized environment. (inspired by [this repository](https://github.com/airscholar/e2e-data-engineering))

And I aim to learn:
- Building and orchestrating pipelines with Apache Airflow
- Real-time data streaming using Apache Kafka (KRaft mode — no Zookeeper)
- Scalable data processing with Apache Spark
- Using PostgreSQL for Airflow metadata storage and Cassandra for processed data
- Containerizing an entire data stack with Docker Compose

## System Architecture

![System Architecture](./system_arch.svg)

Components in this project:
- **Data Source**: `randomuser.me` API generates random user data for the pipeline.
- **Apache Airflow**: Orchestrates the pipeline and stores metadata in PostgreSQL.
- **Apache Kafka (KRaft)**: Backbone for real-time data streaming — no Zookeeper required.
- **Control Center & Schema Registry**: Kafka monitoring and schema management.
- **Apache Spark**: Processes the streamed data (Spark 4.0).
- **Cassandra**: Stores the final processed data.

Stack: Airflow 3.1.8, Python 3.12, Kafka (KRaft), Spark 4.0, Cassandra, PostgreSQL, Docker

## Set Up

1. Clone the repository:
    ```bash
    git clone https://github.com/babuush/streaming-spark-stack.git
    cd streaming-spark-stack
    ```

2. Spin up all services with Docker Compose:
    ```bash
    docker compose up -d
    ```

3. Wait for services to be healthy, then get the generated Airflow admin password from logs:
    ```bash
    docker compose logs api-server | grep "Password for user"
    ```
    Then access the UIs:
    - Airflow UI: http://localhost:8080 (user: `admin`, password: from the command above)
    - Kafka Control Center: http://localhost:9021
    - Spark Master UI: http://localhost:9090

4. Trigger the `user_automation` DAG from the Airflow UI to start producing data to Kafka.

5. Run the Spark streaming job to consume from Kafka and write to Cassandra:
    ```bash
    docker exec -it <spark-master-container> spark-submit \
      --packages com.datastax.spark:spark-cassandra-connector_2.13:3.5.1,org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0 \
      spark_stream.py
    ```

## Services & Ports

| Service          | Port  |
|------------------|-------|
| Airflow API Server (UI) | 8080  |
| Kafka Broker     | 9092  |
| Schema Registry  | 8081  |
| Control Center   | 9021  |
| Spark Master UI  | 9090  |
| Spark Master RPC | 7077  |
| Cassandra        | 9042  |
