import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI

from kafka import KafkaAdminClient
from kafka.admin import NewTopic, ConfigResource, ConfigResourceType
from kafka.errors import (
    KafkaError,
    TopicAlreadyExistsError,
)

# verbose=True will print the environment variables to the console
load_dotenv(verbose=True)

logger = logging.getLogger(__name__)  # logger for the current module

# instance of fastAPI
app = FastAPI()

# global variable for the Kafka admin client
admin_client = None


@app.on_event("startup")
async def startup_event():
    """
    Startup event for the FastAPI application.
    """
    try:
        # create Kafka admin client
        global admin_client
        admin_client = KafkaAdminClient(
            bootstrap_servers=os.getenv("BOOTSTRAP_SERVERS")
        )
        logger.info(f"Kafka admin client created successfully")
        # create topic
        topics = [
            NewTopic(
                name=os.getenv("LOCATION_TOPIC_NAME"),
                num_partitions=int(os.getenv("LOCATION_TOPIC_PARTITION_COUNT")),
                replication_factor=int(os.getenv("LOCATION_TOPIC_REPLICATION_FACTOR")),
            )
        ]
        for topic in topics:
            try:
                # create topic
                admin_client.create_topics([topic])
                logger.info(f"Topic created successfully")
            except TopicAlreadyExistsError as e:
                logger.warning(
                    f"Topic already exists - Updating Topic Configurations Now: {e}"
                )
                # admin_client.alter_topic_configs(topic, {
                #     "cleanup.policy": os.getenv("LOCATION_TOPIC_CLEANUP_POLICY"),
                #     "compression.type": os.getenv("LOCATION_TOPIC_COMPRESSION_TYPE"),
                #     "max.message.bytes": int(os.getenv("LOCATION_TOPIC_MAX_MESSAGE_BYTES")),
                #     "retention.ms": int(os.getenv("LOCATION_TOPIC_RETENTION_TIME")),
                # })
                cfg_resource_update = ConfigResource(
                    ConfigResourceType.TOPIC,
                    os.getenv("LOCATION_TOPIC_NAME"),
                    configs={
                        "cleanup.policy": os.getenv("LOCATION_TOPIC_CLEANUP_POLICY"),
                        "compression.type": os.getenv(
                            "LOCATION_TOPIC_COMPRESSION_TYPE"
                        ),
                        "max.message.bytes": int(
                            os.getenv("LOCATION_TOPIC_MAX_MESSAGE_BYTES")
                        ),
                        "retention.ms": int(os.getenv("LOCATION_TOPIC_RETENTION_TIME")),
                    },
                )
                admin_client.alter_configs([cfg_resource_update])
                logger.info("Topic configurations updated successfully")
            except KafkaError as e:
                logger.error(f"Error updating topic configurations: {e}")
                raise e

    except KafkaError as e:
        logger.error(f"Error creating Kafka admin client: {e}")
        raise e
    finally:
        # close Kafka admin client
        admin_client.close()


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event for the FastAPI application.
    """
    try:
        # close Kafka admin client
        global admin_client
        admin_client.close()
    except KafkaError as e:
        logger.error(f"Error closing Kafka admin client: {e}")
        raise e
    finally:
        # close Kafka admin client
        admin_client.close()


@app.get("/hello-world")
async def hello_world():
    return {"message": "Hello World"}
