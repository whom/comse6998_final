import json, certifi
# from kafka import KafkaProducer
import time
from  elasticsearch import Elasticsearch

ES_ENDPOINT = ('https://search-tap-fashion-ahlt6conoduuuihoeyjqd7olpq.us-west-2.es.amazonaws.com')

# POC on how to create posts.
# When we want to create posts, we collect information on it, then send it to ElasticSearch.
# ElasticSearch automatically assigns an ID to it (unique, hash).


def storePost(post_message):
	es = Elasticsearch([ES_ENDPOINT],
		use_ssl=True,
		verify_certs=True,
		ca_certs=certifi.where(),)

	result = es.index(index='posts', doc_type='post', body=post_message)
	return result['_id']

def createPost(title, user_id, text, location=None, score=0, images=None, comments=None):
	es = Elasticsearch([ES_ENDPOINT],
		use_ssl=True,
		verify_certs=True,
		ca_certs=certifi.where(),)

	post = {}
	post['title'] = title
	post['user_id'] = user_id
	post['text'] = text
	post['score'] = score
	post['location'] = {}
	post['comments'] = []
	post['images'] = []

	if location:
		post['location']['lat'] = location['lat']
		post['location']['lon'] = location['lon']

	if images:
		for image in images:
			post['images'].append(image)

	if comments:
		for comment in comments:
			post['comments'].append(comment)

	return post

def findPost(post_id):
	es = Elasticsearch([ES_ENDPOINT],
		use_ssl=True,
		verify_certs=True,
		ca_certs=certifi.where(),)
		
	results = es.search(index="posts",
		doc_type="post", 
		body={"query":{ "terms": { "_id": [post_id]}}})

	if results['hits']['total'] > 0:
		return results['hits']['hits']

'''
def main():
	producer_test = Postmaster(ES_ENDPOINT, 'test_topic')
	producer_test.createPost(title="HELLO WORLD MY FRIEND!",
		user_id="12345", text="Yep. Something Posted. This is a test", location={'lat':45, 'lon':50})
	post_id = producer_test.run()
	print "Added: " + post_id

	posts = producer_test._producer.search(index="posts", doc_type="post", body={"doc": {"query":{ "match_all": {}}}})

	for post in posts['hits']['hits']:
		print post['_source']

if __name__ == "__main__":
	main()
'''