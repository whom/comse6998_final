import json, logging, certifi
# from kafka import KafkaProducer
import time
from  elasticsearch import Elasticsearch
import post_functions, comment_functions

ES_ENDPOINT = ('https://search-tap-fashion-ahlt6conoduuuihoeyjqd7olpq.us-west-2.es.amazonaws.com')

'''
Builds the entire post, given a post ID.
Accepts a post ID as a string
Returns a fully formed dictionary object that contains the full post, including
all comments (rather than comment IDs)

Note: Not sure if we need this. What about resolving user IDs to user names?
'''
def buildWholePost(post_id):
	post = post_functions.findPost(post_id)

	if post:
		comments = post.pop('comments')
		post['comments'] = []

		for comment in comments:
			print comment
			comment_body = comment_functions.findComment(comment)
			post['comments'].append(comment_body)

		return post
	else:
		return None

def getAllPosts():
	results = []

	es = Elasticsearch([ES_ENDPOINT], use_ssl=True, verify_certs=True,
		ca_certs=certifi.where(),)
	res = es.search(index="posts", doc_type="post", search_type='scan',
		scroll='2m', size=10, body={"query": {"match_all": {}}})

	sid = res['_scroll_id']
	scroll_size = res['hits']['total']

	while scroll_size > 0:
		res = es.scroll(scroll_id=sid, scroll='2m')
		sid = res['_scroll_id']
		scroll_size = len(res['hits']['hits'])

		for doc in res['hits']['hits']:
			clean = doc['_source']
			clean['post_id'] = doc['_id']
			results.append(clean)

	return results

def getPost():
	results = []

	es = Elasticsearch([ES_ENDPOINT], use_ssl=True, verify_certs=True,
		ca_certs=certifi.where(),)
	res = es.get(index="posts", doc_type='post', id='AVjMtr7gCBwe55JHWopg')

	clean = res['_source']
	clean['post_id'] = res['_id']
	results.append(clean)

	return results


def get_searched_posts(search_str):
   results = []

   es = Elasticsearch([ES_ENDPOINT], use_ssl=True, verify_certs=True,
       ca_certs=certifi.where(),)
   res = es.search(index="posts", doc_type="post", search_type='scan',
       scroll='2m', size=10, body={"query": {"match": {"title": "%"+search_str+"%"}}})

   sid = res['_scroll_id']
   scroll_size = res['hits']['total']

   while scroll_size > 0:
       res = es.scroll(scroll_id=sid, scroll='2m')
       sid = res['_scroll_id']
       scroll_size = len(res['hits']['hits'])

       for doc in res['hits']['hits']:
           clean = doc['_source']
           clean['post_id'] = doc['_id']
           results.append(clean)

   return results
   
'''
Note: We're grabbing comments one at a time. However, we can dump all the IDs
into ElasticSearch as a list which will be quicker. But we can visit this
later.
'''
