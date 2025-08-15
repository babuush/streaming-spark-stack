import logging

from cassandra.cluster import Cluster
from pyspark.sql import SparkSession

# from pyspark.sql.functions import from_json, col
# from pyspark.sql.types import StructType, StructField, StringType


def create_keyspace(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS spark_streams
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
    """)

    print("Keyspace created successfully!")


def create_table(session):
    pass


def insert_data(session, **kwargs):
    pass


def create_spark_connection():
    s_conn = None

    try:
        s_conn = (
            SparkSession.builder.appName("SparkDataStreaming")
            .config(
                "spark.jars.packages",
                "com.datastax.spark:spark-cassandra-connector_2.13:3.41",
                "org.apache.spark:spark-sql-kafka-0-10_2.13:3.4.1",
            )
            .config("spark.cassandra.connection.host", "localhost")
            .getOrCreate()
        )

        s_conn.sparkContext.setLogLevel("Error")
        logging.info("Spark connection create successfully")
    except Exception as e:
        logging.error(f"Couldn't create the spark session due to exception {e}")

    return s_conn


def create_cassandra_connection():
    try:
        cluster = Cluster(["localhost"])
        cassandra_session = cluster.connect()

        return cassandra_session
    except Exception as e:
        logging.error(f"Could not create cassandra session due to {e}")
        return None


if __name__ == "__main__":
    # create spark connection
    spark_conn = create_spark_connection()

    if spark_conn is not None:
        session = create_cassandra_connection()

        if session is not None:
            create_keyspace(session)
            create_table(session)
