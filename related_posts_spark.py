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
[[post ID, similarity score], ...]
'''
import certifi, json, string, logging, re, string
from pyspark import SparkConf, SparkContext
from elasticsearch import Elasticsearch
from pprint import pprint
from gensim import corpora, models, similarities

ENDPOINT = ('https://search-tap-fashion-ahlt6conoduuuihoeyjqd7olpq.us-west-2'
    '.es.amazonaws.com')
EVALUATED_POSTS = {}
APP_NAME = "Related Posts"
MASTER = "local[*]"
CORPUS_PATH = "/tmp/corpus.mm"
DICTIONARY_PATH = "/tmp/dictionary.dict"
es = None

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

# grab all posts
def grabPosts():
  results = []

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

def combine_text_and_title(post):
  return [post['post_id'], '{0} {1}'.format(post['title'], post['text'])]

def main():
  conf = SparkConf().setAppName(APP_NAME).setMaster(MASTER)
  sc = SparkContext(conf=conf)
  posts = grabPosts()
  posts_rdd = sc.parallelize(posts)
  posts_combined = (posts_rdd.map(lambda x: combine_text_and_title(x))
      .collectAsMap())

  keys = posts_combined.keys()
  documents_rdd = sc.parallelize(posts_combined.values())

  # sanitize and build our corpus
  sentences = documents_rdd.map(lambda x: sanitize_sentence(x))
  dictionary = corpora.Dictionary(sentences.collect())
  dictionary.save(DICTIONARY_PATH)
  corpus = sentences.map(lambda x: dictionary.doc2bow(x)).collect()
  corpora.MmCorpus.serialize(CORPUS_PATH, corpus)

  # find out how many features we have and train the model.
  # save the corpus as well for later use.
  last_corpus = corpus[len(corpus) - 1]
  num_features = last_corpus[len(last_corpus) - 1][0] + 1
  tfidf = models.TfidfModel(corpus)
  index = similarities.SparseMatrixSimilarity(tfidf[corpus],
      num_features=num_features)

  # now that the corpus is settled, go through each post and compute similarity.
  # then store the results in elastic search.

  for key, value in posts_combined.iteritems():
    storage = {}
    vec = dictionary.doc2bow(sanitize_sentence(value))
    sims = index[tfidf[vec]]
    p = list(enumerate(sims))
    top_ten = sorted(p, key=lambda x: x[1], reverse=True)[1:11]
    top_ten = [list(x) for x in top_ten]
    dic = [{'post_id':keys[x[0]], 'score':float(x[1])} for x in top_ten]
    EVALUATED_POSTS[key] = dic

    storage['id'] = key
    storage['related_posts'] = dic
    es.index(index='related_posts', doc_type='post', id=key, body=storage)

  return EVALUATED_POSTS

if __name__ == "__main__":
  es = Elasticsearch([ENDPOINT], use_ssl=True, verify_certs=True,
    ca_certs=certifi.where(),)
  main()
