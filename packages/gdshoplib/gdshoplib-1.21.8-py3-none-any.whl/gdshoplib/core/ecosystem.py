import time
from typing import Optional

import orjson as json
from kafka import KafkaProducer
from loguru import logger
from pydantic import BaseModel


def save(topic, iterator, parser):
    producer = KafkaProducer(
        bootstrap_servers=NotionSettings().KAFKA_BROKER,
        value_serializer=lambda m: json.dumps(m),
        request_timeout_ms=1000,
    )

    class Message(BaseModel):
        data: dict
        timestamp: int
        data_md5: Optional[str]
        message_type: str

        def send(self):
            # - Отправить в kafka
            future = producer.send(topic, self.dict())
            try:
                future.get(timeout=10)
            except KafkaError as e:
                # Decide what to do if produce request failed...
                logger.exception(e)

    result = {"all": []}

    for page in iterator:
        if not result.get(page["object"]):
            result[page["object"]] = []

        result[page["object"]].append(page["id"])
        result["all"].append(page["id"])

    Message(data=result, timestamp=int(time.time()), message_type="scan").send()
    logger.info(f"Count: {len(result)}")
