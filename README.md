# streaming-spark-stack

## Introduction & Learning Goals
This repository is my personal learning project where I practice building an end-to-end data engineering pipeline that demonstrates the flow of data from ingestion to streaming, processing, and finally storage, all within a containerized environment.. (inspired by [this repository](https://github.com/airscholar/e2e-data-engineering)) 

And I aim to learn:
- Building and orchestrating pipelines with Apache Airflow
- Real-time data streaming using Apache Kafka
- Distributed coordination with Zookeeper
- Scalable data processing with Apache Spark
- Using PostgreSQL for raw data storage and Cassandra for processed data
- Containerizing an entire data stack with Docker Compose

## System Architecture

Components in this project:
- Apache Airflow – Orchestrates the pipeline and stores raw data in PostgreSQL
- Apache Kafka + Zookeeper – Backbone for real-time data streaming
- Control Center & Schema Registry – For Kafka monitoring and schema management
- Apache Spark – Processes the streamed data
- Cassandra – Stores the final processed data

Stack Overview: Airflow, Python, Kafka, Zookeeper, Spark, Cassandra, PostgreSQL, Docker

## Set Up

1. Clone the repository:
    ```bash
    git clone https://github.com/babuush/streaming-spark-stack.git
    ```

2. Navigate to the project directory:
    ```bash
    cd streaming-spark-stack
    ```

3. Install dependencies (if running services locally instead of Docker):
    ```bash
    pip3 install apache-airflow kafka-python spark pyspark cassandra-driver
    ```

4. Spin up all services with Docker Compose:
    ```bash
    docker-compose up
    ```
