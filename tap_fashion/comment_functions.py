import json, logging, threading, certifi
# from kafka import KafkaConsumer
import time
from  elasticsearch import Elasticsearch
# imported just for the example.
from post_functions import Postmaster

ES_ENDPOINT = ('https://search-fashion-exembdm6hi7dy6gxjhubkplo2i.us-west-2.es.amazonaws.com')

# POC of storing and retrieving comments.
# comments cannot be exist on their own. They must be part of a post.
# Therefore, in order to add a comment, we must first have a post to add it to.
# It's a little more complicated than posts.

class Commentmaster(threading.Thread):
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
			result = self._producer.index(index='comments',doc_type='comment', body=self._message)

			# update the post with this new comment
			posts = self._producer.search(index="posts", 
				doc_type="post", 
				body={"query":{ "terms": {"_id":["{}".format(self._message['post_id'])]}}})

			if posts['hits']['total'] == 1:
				for post in posts['hits']['hits']:
					post['_source']['comments'].append(result['_id']) 

					post_update = self._producer.update(index="posts",
						doc_type="post", id=self._message['post_id'],
						body={"doc": {"comments": post['_source']['comments']}})

			self._message = {}
			return result['_id']
		else:
			return None

	def createComment(self, post_id, user_id, text, location=None, score=0, images=None):
		self._message['user_id'] = user_id
		self._message['text'] = text
		self._message['score'] = score
		self._message['post_id'] = post_id
		self._message['images'] = []
		self._message['location'] = {}

		if location:
			self._message['location']['lat'] = location['lat']
			self._message['location']['lon'] = location['lon']

		if images:
			for image in images:
				self._message['images'].append({'url':image})

	def findComment(self,  comment_id):
		results = self._producer.search(index="comments",
			doc_type="comment", 
			body={"query":{ "terms": { "_id": ["{}".format(comment_id)]}}})

		if results['hits']['total'] > 0:
			return results['hits']['hits']



def main():
	comment_test = Commentmaster(ES_ENDPOINT, 'test_topic')
	post_test = Postmaster(ES_ENDPOINT, 'test_topic')

	comment_test.createComment(post_id="AVhgNKzZqbgLShExm8cr", text="HELLO WORLD! THIS IS DIFFERENT!",
		user_id="12345", location={'lat':45, 'lon':50})
	comment_test.run()

	comments = post_test._producer.search(index="posts", doc_type="post", body={"query":{ "terms": { "_id": ["AVhgNKzZqbgLShExm8cr"]}}})

	for comment in comments['hits']['hits']:
		comment_id = comment['_source']['comments']

		for c in comment_id:
			text = comment_test._producer.search(index="comments", doc_type="comment", body={"query":{ "terms": { "_id": [c]}}})
			print text['hits']['hits']


if __name__ == "__main__":
	main()