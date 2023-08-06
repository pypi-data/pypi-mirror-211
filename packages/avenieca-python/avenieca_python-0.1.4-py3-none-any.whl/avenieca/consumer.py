import json
from kafka import KafkaConsumer

from avenieca import Broker


class Consumer:
    """
    Base consumer for consuming messages (signals) from a digital twin.

    :param config: configuration dictionary
    """
    def __init__(self,
                 config: Broker,
                 ):
        self.config = config
        self.topic = config.pub_topic
        self.client = KafkaConsumer(
            self.topic,
            bootstrap_servers=config.url,
            auto_offset_reset=config.auto_offset_reset
        )

    def consume(self, func, sync_once=False):
        """
        :param func: handler to process received messages
        :param sync_once: run consume loop once
        :return: None
        """
        for msg in self.client:
            byte_val = msg.value
            data = json.loads(byte_val)
            func(data)
            if sync_once:
                break
