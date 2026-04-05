import uuid
from datetime import datetime

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.standard.operators.python import PythonOperator

default_args = {"owner": "babuush", "start_date": datetime(2025, 8, 15, 15, 00)}


def get_data():
    import requests

    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res["results"][0]

    return res


def format_data(res):
    data = {}
    location = res["location"]
    data["id"] = str(uuid.uuid4())
    data["first_name"] = res["name"]["first"]
    data["last_name"] = res["name"]["last"]
    data["gender"] = res["gender"]
    data["address"] = (
        f"{str(location['street']['number'])} {location['street']['name']}, "
        f"{location['city']}, {location['state']}, {location['country']}"
    )
    data["post_code"] = location["postcode"]
    data["email"] = res["email"]
    data["username"] = res["login"]["username"]
    data["dob"] = res["dob"]["date"]
    data["registered_date"] = res["registered"]["date"]
    data["phone"] = res["phone"]
    data["picture"] = res["picture"]["medium"]

    return data


def stream_data():
    import json
    import logging
    import time

    from kafka import KafkaProducer

    producer = KafkaProducer(bootstrap_servers=["broker:29092"], max_block_ms=5000)
    current_time = time.time()

    while True:
        if time.time() > current_time + 60:
            break
        try:
            res = get_data()
            res = format_data(res)
            producer.send("users_created", json.dumps(res).encode("utf-8"))
        except Exception as e:
            logging.error(f"Error: {e}")
            continue


with DAG(
    "user_automation",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:
    produce_to_kafka = PythonOperator(
        task_id="stream_data_from_api", python_callable=stream_data
    )

    # Drains the Kafka backlog into Cassandra using Structured Streaming with
    # Trigger.AvailableNow, so the task terminates once the current batch of
    # messages has been processed (instead of running forever).
    stream_to_cassandra = SparkSubmitOperator(
        task_id="stream_to_cassandra",
        application="/opt/airflow/spark_stream.py",
        conn_id="spark_default",
        packages=(
            "com.datastax.spark:spark-cassandra-connector_2.13:3.5.1,"
            "org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0"
        ),
        conf={
            "spark.jars.ivy": "/tmp/.ivy2",
            "spark.driver.extraJavaOptions": "-Djava.net.preferIPv4Stack=true",
            "spark.executor.extraJavaOptions": "-Djava.net.preferIPv4Stack=true",
        },
        verbose=False,
    )

    produce_to_kafka >> stream_to_cassandra
