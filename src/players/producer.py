import json
from typing import Optional, List
import logging

from kafka import KafkaProducer

from ..config import kafka_settings

logging.basicConfig(format='%(levelname)s:%(message)s')

producer = KafkaProducer(
    bootstrap_servers=f"{kafka_settings.hostname}:{kafka_settings.port}",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def on_send_success(record_metadata):
    logging.info(f"Message n°{record_metadata.offset} send on topic {record_metadata.topic}")

def on_send_error(excp):
    logging.error('Error when sending', exc_info=excp)

async def produce_flag(name: str, code_name: str, flag: str, tags: Optional[List[str]]):
    message = {
        "team_name": name,
        "team_code_name": code_name,
        "flag_name": flag,
        "tags": tags
    }
    producer.send(kafka_settings.topic, value=message).add_callback(on_send_success).add_errback(on_send_error)
