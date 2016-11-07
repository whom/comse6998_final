import json, logging, threading
from kafka import KafkaClient, SimpleConsumer

class TapFashionConsumer(threading.Thread):
	daemon = True

	def __init__(self, zk_endpoint, topic):
		self._topic = topic
		self._kafka = KafkaClient(zk_endpoint)
		self._producer = SimpleProducer(self._kafka)
		self._message = {}
		self._counter = 0