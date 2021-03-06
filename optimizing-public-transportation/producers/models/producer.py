"""Producer base-class providing common utilites and functionality"""
import logging
import time

from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer

logger = logging.getLogger(__name__)


class Producer:
    """Defines and provides common functionality amongst Producers"""

    # Tracks existing topics across all Producer instances
    existing_topics = set([])
    broker_url: str = "PLAINTEXT://localhost:9092"
    schema_registry_url: str = "http://localhost:8081"

    def __init__(
            self,
            topic_name,
            key_schema,
            value_schema=None,
            num_partitions=1,
            num_replicas=1,
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas

        self.broker_properties = {
            "bootstrap.servers": self.broker_url,
            "schema.registry.url": self.schema_registry_url,
        }

        self.admin_client = AdminClient({"bootstrap.servers": self.broker_url})

        # If the topic does not already exist, try to create it
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        self.producer = AvroProducer(self.broker_properties,
                                     default_key_schema=self.key_schema,
                                     default_value_schema=self.value_schema)

    def create_topic(self):
        if self.topic_created():
            return

        future_map = self.admin_client.create_topics([
            NewTopic(
                topic=self.topic_name,
                num_partitions=self.num_partitions,
                replication_factor=self.num_replicas
            )
        ])

        for topic, future in future_map.items():
            try:
                future.result()
                logger.info(f"{self.topic_name} is created")
            except Exception as e:
                logger.error(f"{self.topic_name} is not created: {e}")

    def topic_created(self):
        topic_props = self.admin_client.list_topics(timeout=5)
        topic_names = set(topic.topic for topic in iter(topic_props.topics.values()))
        return self.topic_name in topic_names

    def time_millis(self):
        return int(round(time.time() * 1000))

    def close(self):
        self.producer.flush(timeout=5)

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
