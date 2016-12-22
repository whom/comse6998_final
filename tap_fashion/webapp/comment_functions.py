import json, certifi
from boto import sqs
from boto.sqs.message import Message
# from kafka import KafkaConsumer
import time
from  elasticsearch import Elasticsearch

ES_ENDPOINT = ('https://search-tap-fashion-ahlt6conoduuuihoeyjqd7olpq.us-west-2.es.amazonaws.com')

# POC of storing and retrieving comments.
# comments cannot be exist on their own. They must be part of a post.
# Therefore, in order to add a comment, we must first have a post to add it to.
# It's a little more complicated than posts.

conf = {
  'sqs-access-key': 'AKIAIP3UK2QLTBYKEWXQ',
  'sqs-secret-key': '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',
  'sqs-queue-name': 'comments-queue',
  'sqs-region': 'us-west-2'
}

''' Stores the comment in ElasticSearch, then updates the post with this comment ID.
'''
def storeComment(comment_message):
	print "Storing comment: " + json.dumps(comment_message)
	es = Elasticsearch([ES_ENDPOINT],
		use_ssl=True,
		verify_certs=True,
		ca_certs=certifi.where(),)

	sqs_client =  sqs.connect_to_region(conf.get('sqs-region'),
    	aws_access_key_id=conf.get('sqs-access-key'),
    	aws_secret_access_key =conf.get('sqs-secret-key'))

	sqs_queue = sqs_client.get_queue(conf.get('sqs-queue-name'))
	message = Message()

	# update the post with this new comment
	posts = es.search(index="posts", doc_type="post", 
		body={"query":{ "terms": {"_id":[comment_message['post_id']]}}})

	if posts['hits']['total'] == 1:
		for post in posts['hits']['hits']:
			full_message = {}
			full_message['post'] = post
			full_message['comment'] = comment_message

			message.set_body(json.dumps(full_message))
			status = sqs_queue.write(message)

''' Creates and returns a dictionary object with comments.
'''
def createComment(post_id, user_id, user_name, text, location=None, score=0, images=None):
	print "Creating comment for post " + post_id
	es = Elasticsearch([ES_ENDPOINT],
		use_ssl=True,
		verify_certs=True,
		ca_certs=certifi.where(),)

	comment = {}
	comment['user_id'] = user_id
	comment['user_name'] = user_name
	comment['text'] = text
	comment['post_id'] = post_id
	comment['location'] = {}


	# not implemented or used
	comment['score'] = score
	comment['images'] = []
	if images:
		for image in images:
			comment['images'].append({'url':image})

	if location:
		comment['location']['lat'] = location['lat']
		comment['location']['lon'] = location['lon']

	return comment

''' Retrieves a comment given a specific ID.
'''
def findComment(comment_id):
	es = Elasticsearch([ES_ENDPOINT],
		use_ssl=True,
		verify_certs=True,
		ca_certs=certifi.where(),)

	results = es.search(index="comments",
		doc_type="comment", 
		body={"query":{ "terms": { "_id": ["{}".format(comment_id)]}}})

	if results['hits']['total'] > 0:
		result = results['hits']['hits'][0]['_source']
		object_id = results['hits']['hits'][0]['_id']
		result['post_id'] = object_id
		return result
	else:
		return None

'''
def main():
	test = comment_test.createComment(post_id="AVhgNKzZqbgLShExm8cr", text="HELLO WORLD! THIS IS DIFFERENT!",
		user_id="12345", location={'lat':45, 'lon':50})
	comment_test.storeComment(test)

	comments = es.search(index="posts", doc_type="post", body={"query":{ "terms": { "_id": ["AVhgNKzZqbgLShExm8cr"]}}})

	for comment in comments['hits']['hits']:
		comment_id = comment['_source']['comments']

		for c in comment_id:
			text = es.search(index="comments", doc_type="comment", body={"query":{ "terms": { "_id": [c]}}})
			print text['hits']['hits']


if __name__ == "__main__":
	main()
'''