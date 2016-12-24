import boto, json, threading, certifi
from boto import sqs
from elasticsearch import Elasticsearch

ES_ENDPOINT = ('https://search-tap-fashion-ahlt6conoduuuihoeyjqd7olpq.us-west-2.es.amazonaws.com')

conf = {
  'sqs-access-key': 'AKIAIP3UK2QLTBYKEWXQ',
  'sqs-secret-key': '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',
  'sqs-region': 'us-west-2'
}

def main(queue_name, index, doc_type):
    print "Starting up " + index + " " + doc_type
    awsSQS = sqs.connect_to_region(conf.get('sqs-region'),
		aws_access_key_id=conf.get('sqs-access-key'),
		aws_secret_access_key =conf.get('sqs-secret-key'))
	
    es = Elasticsearch([ES_ENDPOINT], use_ssl=True,
		verify_certs=True, ca_certs=certifi.where(),)

    q = awsSQS.create_queue(queue_name)
    
    while True:
	    messages = q.get_messages()
	    if messages:
		        print queue_name

			for message in messages:
			    msg = json.loads(message.get_body())

		    	if queue_name == 'posts-queue':
		    		result = es.index(index='posts', doc_type='post',
		    			body=msg)
		    		print "Stored new post as {0}".format(result['_id'])
		    		print "Post: " + result
		    	else:
		    		post = msg['post']
		    		comment = msg['comment']

	    			result = es.index(index='comments',doc_type='comment', body=comment)
	    			post['_source']['comments'].append(result['_id'])
	    			print "Stored new comment for post {0} as {1}".format(result['_id'], post['_id'])
	    			print "Comment: " + result

	    			es.update(index="posts", doc_type="post", id=post['_id'], body={"doc": {"comments": post['_source']['comments']}})

    			q.delete_message(message)

if __name__ == "__main__":
	t = threading.Thread(target=main, args=('posts-queue', 'posts', 'post',))
	t.start()
	q = threading.Thread(target=main, args=('comments-queue', 'comments', 'comment',))
	q.start()
