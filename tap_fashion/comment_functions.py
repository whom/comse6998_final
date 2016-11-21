import json, certifi
# from kafka import KafkaConsumer
import time
from  elasticsearch import Elasticsearch

ES_ENDPOINT = ('https://search-tap-fashion-ahlt6conoduuuihoeyjqd7olpq.us-west-2.es.amazonaws.com')

# POC of storing and retrieving comments.
# comments cannot be exist on their own. They must be part of a post.
# Therefore, in order to add a comment, we must first have a post to add it to.
# It's a little more complicated than posts.

''' Stores the comment in ElasticSearch, then updates the post with this comment ID.
'''
def storeComment(comment_message):
	es = Elasticsearch([ES_ENDPOINT],
		use_ssl=True,
		verify_certs=True,
		ca_certs=certifi.where(),)

	result = es.index(index='comments',doc_type='comment', body=comment_message)

	# update the post with this new comment
	posts = es.search(index="posts", doc_type="post", 
		body={"query":{ "terms": {"_id":[comment_message['post_id']]}}})

	if posts['hits']['total'] == 1:
		for post in posts['hits']['hits']:
			post['_source']['comments'].append(result['_id']) 

			post_update = es.update(index="posts",
				doc_type="post", id=comment_message['post_id'],
				body={"doc": {"comments": post['_source']['comments']}})

	return result['_id']

''' Creates and returns a dictionary object with comments.
'''
def createComment(post_id, user_id, user_name, text, location=None, score=0, images=None):
	es = Elasticsearch([ES_ENDPOINT],
		use_ssl=True,
		verify_certs=True,
		ca_certs=certifi.where(),)

	comment = {}
	comment['user_id'] = user_id
	comment['user_name'] = user_name
	comment['text'] = text
	comment['score'] = score
	comment['post_id'] = post_id
	comment['images'] = []
	comment['location'] = {}

	if location:
		comment['location']['lat'] = location['lat']
		comment['location']['lon'] = location['lon']

	if images:
		for image in images:
			comment['images'].append({'url':image})

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
		return results['hits']['hits']

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