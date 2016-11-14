import json, logging, threading, certifi
# from kafka import KafkaProducer
import time
from  elasticsearch import Elasticsearch

ES_ENDPOINT = ('https://search-fashion-exembdm6hi7dy6gxjhubkplo2i.us-west-2.es.amazonaws.com')

# POC on how to create posts.
# When we want to create posts, we collect information on it, then send it to ElasticSearch.
# ElasticSearch automatically assigns an ID to it (unique, hash).

class Postmaster(threading.Thread):
	daemon = True

	def __init__(self, endpoint, topic):
		self._topic = topic
		self._message = {}
		self._producer = Elasticsearch([endpoint],
			use_ssl=True,
			verify_certs=True,
			ca_certs=certifi.where(),) 

	def run(self):
		if self._message:
			result = self._producer.index(index='posts', doc_type='post', body=self._message)
			self._message = {}

			return result['_id']
		else:
			return None

	def createPost(self, title, user_id, text, location=None, score=0, images=None, comments=None):
		self._message['title'] = title
		self._message['user_id'] = user_id
		self._message['text'] = text
		self._message['score'] = score
		self._message['location'] = {}
		self._message['comments'] = []
		self._message['images'] = []

		if location:
			self._message['location']['lat'] = location['lat']
			self._message['location']['lon'] = location['lon']

		if images:
			for image in images:
				self._message['images'].append(image)

		if comments:
			for comment in comments:
				self._message['comments'].append(comment)

	def findPost(self, post_id):
		results = self._producer.search(index="posts",
			doc_type="post", 
			body={"query":{ "terms": { "_id": ["{}".format(post_id)]}}})

		if results['hits']['total'] > 0:
			return results['hits']['hits']



def main():
	producer_test = Postmaster(ES_ENDPOINT, 'test_topic')
	producer_test.createPost(title="HELLO WORLD MY FRIEND!",
		user_id="12345", text="Yep. Something Posted. This is a test", location={'lat':45, 'lon':50})
	post_id = producer_test.run()
	print "Added: " + post_id

	posts = producer_test._producer.search(index="posts", doc_type="post", body={"query":{ "match_all": {}}})

	for post in posts['hits']['hits']:
		print post['_source']

if __name__ == "__main__":
	main()