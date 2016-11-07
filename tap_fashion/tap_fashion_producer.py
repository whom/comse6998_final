import json, logging, threading
from kafka import KafkaProducer
import time

class TapFashionProducer(threading.Thread):
	daemon = True

	def __init__(self, zk_endpoint, topic):
		self._topic = topic
		self._producer = KafkaProducer(bootstrap_servers=zk_endpoint)
		self._message = {}
		self._counter = 0

	def run(self):
		while True:
			if self._message:
				self._producer.send(self._topic, bytes(json.dumps(self._message)))
				self._counter += 1
				self._message = {}

	def createPost(self, title, user_id, text, location=None, score=0, images=None, comments=None):
		self._message['title'] = title
		self._message['user_id'] = user_id
		self._message['post_id'] = ('00000000' + str(self._counter))[-9:]
		self._message['text'] = text
		self._message['score'] = score

		if location:
			self._message['location'] = {}
			self._message['location']['lat'] = location['lat']
			self._message['location']['lon'] = location['lon']

		if images:
			self._message['images'] = []
			for image in images:
				self._message['images'].append({'url':image})

		if comments:
			self._message['comments'] = []
			for comment in comments:
				self._message['comments'].append({'comment_id':comment})


def main():
	producer_test = TapFashionProducer('localhost:9092', 'test_topic')
	producer_test.createPost(title="HELLO WORLD!", user_id="12345", text="Yep.", location={'lat':45, 'lon':50})
	producer_test.run()

if __name__ == "__main__":
	main()