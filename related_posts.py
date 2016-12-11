''' HOW DOES THIS WORK??

1. Retrieve all posts from ElasticSearch. Combine the text and title, then
sanitize the information by removing punctuation, stop words, and http links.
2. Using gensim, build a corpus using the remaining text.
3. Transform the corpus into a TF-IDF model and index it.
4. With the model complete, now we go through every single post and evaluate
similarity scores.
4a. Sanitize the post, then transform it into a sparse matrix.
4b. Run it against our model.
4c. Save the top 10 similarities for the post into EVALUATED_POSTS.
5. Profit?!

Results are stored in dictionary format:
key = post ID
value = Sorted list of 10 most related post IDs, along with their similarity
scores. It is in this form:
[(post ID, similarity score), ...]
'''

from elasticsearch import Elasticsearch
import certifi, json, string, logging, re, string
from pprint import pprint
from gensim import corpora, models, similarities

ENDPOINT = ('https://search-tap-fashion-ahlt6conoduuuihoeyjqd7olpq.us-west-2'
    '.es.amazonaws.com')
EVALUATED_POSTS = {}

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

# grab all posts
def grabPosts():
  results = []
  es = Elasticsearch([ENDPOINT], use_ssl=True, verify_certs=True,
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
      results.append({'post_id':doc['_id'],'title':doc['_source']['title'],
          'text':doc['_source']['text']})
  
  return results

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

def main():
  posts = grabPosts()
  posts_combined = {x['post_id']: '{0} {1}'.format(x['title'],
      x['text']) for x in posts}

  keys = posts_combined.keys()
  documents = posts_combined.values()

  # sanitize and build our corpus
  sentences = [sanitize_sentence(sentence) for sentence in documents]
  dictionary = corpora.Dictionary(sentences)
  corpus = [dictionary.doc2bow(sentence) for sentence in sentences]

  # find out how many features we have and train the model.
  last_corpus = corpus[len(corpus) - 1]
  num_features = last_corpus[len(last_corpus) - 1][0] + 1
  tfidf = models.TfidfModel(corpus)
  index = similarities.SparseMatrixSimilarity(tfidf[corpus],
      num_features=num_features)

  # now that the corpus is settled, go through each post and compute similarity.
  for key, value in posts_combined.iteritems():
    vec = dictionary.doc2bow(sanitize_sentence(value))
    sims = index[tfidf[vec]]
    p = list(enumerate(sims))
    top_ten = sorted(p, key=lambda x: x[1], reverse=True)[1:11]
    dic = sorted([(keys[x[0]], x[1]) for x in top_ten], key=lambda x: x[1],
        reverse=True)
    EVALUATED_POSTS[key] = dic

  # store in elasticsearch, maybe?

if __name__ == "__main__":
  main()

  print EVALUATED_POSTS