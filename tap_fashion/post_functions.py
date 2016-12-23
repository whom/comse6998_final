import json, certifi, string
from boto import sqs
from boto.sqs.message import Message
# from kafka import KafkaProducer
from  elasticsearch import Elasticsearch
from datetime import datetime
# from gensim import corpora, models, similarities

ES_ENDPOINT = ('https://search-tap-fashion-ahlt6conoduuuihoeyjqd7olpq.us-west-2.es.amazonaws.com')
CORPUS_PATH = "/tmp/corpus.mm"
DICTIONARY_PATH = "/tmp/dictionary.dict"

conf = {
  'sqs-access-key': 'AKIAIP3UK2QLTBYKEWXQ',
  'sqs-secret-key': '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',
  'sqs-queue-name': 'posts-queue',
  'sqs-region': 'us-west-2'
}
'''
def is_number(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def sanitize_sentence(x):
  stoplist = set('for a of the and to in'.split())
  s = x.lower().split()
  s = [w.translate(None, string.punctuation) for w in s]
  s = [w for w in s if w not in stoplist]
  s = [w for w in s if 'http' not in w and not is_number(w)]
  return s


In instances where a related post isn't found, then calculate it.
Then store it.
Returns a list of dictionaries where there are two keys:
post_id: post ID that the post is related to
score: the score our system gave it.

DOESN'T WORK. The module returns the document index, not the ID...
Will need a complete rework in order to calculate in realtime...

def calculateRelatedPosts(post_id):
	es = Elasticsearch([ES_ENDPOINT],
		use_ssl=True,
		verify_certs=True,
		ca_certs=certifi.where(),)

	storage = {}
	post = findPost(post_id)
	dictionary = corpora.Dictionary.load('/tmp/dictionary.dict')
	corpus = corpora.MmCorpus('/tmp/corpus.mm')
	last_corpus = corpus[len(corpus) - 1]
	num_features = last_corpus[len(last_corpus) - 1][0] + 1
	tfidf = models.TfidfModel(corpus)
	index = similarities.SparseMatrixSimilarity(tfidf[corpus],
  		num_features=num_features)

	full_text = '{0} {1}'.format(post['title'], post['text'])
	vec = dictionary.doc2bow(sanitize_sentence(full_text))
	sims = index[tfidf[vec]]
	p = list(enumerate(sims))
	top_ten = sorted(p, key=lambda x: x[1], reverse=True)[1:11]
	top_ten = [list(x) for x in top_ten]
	dic = [{'post_id':x[0], 'score':float(x[1])} for x in top_ten]
	storage['id'] = post_id
	storage['related_posts'] = dic
#	es.index(index='related_posts', doc_type='post', id=post_id, body=storage)
	return dic
'''

'''
For a given post, find the set of 10 related posts. If none exist, then calculate it.
'''
def findRelatedPosts(post_id):
	es = Elasticsearch([ES_ENDPOINT],
		use_ssl=True,
		verify_certs=True,
		ca_certs=certifi.where(),)

	results = es.search(index="related_posts",
		doc_type="post", 
		body={"query":{ "terms": { "_id": [post_id]}}})

	if results['hits']['total'] > 0:
		return results['hits']['hits'][0]['_source']
	else:
		return None

def storePost(post_message):
	print "LOL"
    sqs_client =  sqs.connect_to_region(conf.get('sqs-region'),
      aws_access_key_id=conf.get('sqs-access-key'),
      aws_secret_access_key =conf.get('sqs-secret-key'))

    sqs_queue = sqs_client.get_queue(conf.get('sqs-queue-name'))
    message = Message()
    message.set_body(json.dumps(post_message))
    status = sqs_queue.write(message)

def createPost(title, user_id, text, user_name, location=None, score=0, images=None, comments=None):
	print "Creating a new post!"
	post = {}
	post['title'] = title
	post['user_id'] = user_id
	post['user_name'] = user_name
	post['text'] = text
	post['score'] = score
	post['location'] = {}
	post['comments'] = []
	post['images'] = []
	post['published'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

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
		result = results['hits']['hits'][0]['_source']
		object_id = results['hits']['hits'][0]['_id']
		result['post_id'] = object_id
		return result
	else:
		return None

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