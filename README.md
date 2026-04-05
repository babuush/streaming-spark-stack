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

2. Create your local `.env` from the example (`.env` is git-ignored; these defaults are local-dev only, do not reuse them elsewhere):
    ```bash
    cp .env.example .env
    ```

3. Spin up all services with Docker Compose (first run builds the custom Airflow image):
    ```bash
    docker compose up -d --build
    ```
    > Requires Docker Desktop with **≥ 6 GB** memory allocated.

4. Wait for services to be healthy, then get the generated Airflow admin password from logs:
    ```bash
    docker compose logs api-server | grep "Password for user"
    ```
    Then access the UIs:
    - Airflow UI: http://localhost:8080 (user: `admin`, password: from the command above)
    - Kafka Control Center: http://localhost:9021
    - Spark Master UI: http://localhost:9090

5. Trigger the `user_automation` DAG from the Airflow UI. It runs two tasks:
    - `stream_data_from_api` — produces 60s worth of fake users to the `users_created` Kafka topic.
    - `stream_to_cassandra` — submits `spark_stream.py` to the Spark cluster via `SparkSubmitOperator`, which drains the Kafka topic into the `spark_streams.created_users` Cassandra table (using `Trigger.AvailableNow`, so it exits when the backlog is clear).

6. Verify the data landed in Cassandra:
    ```bash
    docker exec cassandra cqlsh -e "SELECT COUNT(*) FROM spark_streams.created_users;"
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
