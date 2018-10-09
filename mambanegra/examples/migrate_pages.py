# requirements.locked.txt:
# cassandra-driver==3.7.1
# futures==3.0.5
# lru-dict==1.1.6
# pymongo==3.4.0
# six==1.10.0
#
# pip install virtualenv
# virtualenv venv
# source venv/bin/activate
# pip install -r requirements.locked.txt


import os
from bson import CodecOptions
from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.policies import DCAwareRoundRobinPolicy
from datetime import datetime
# from lru import LRU
from pymongo import MongoClient
from six import string_types
from time import gmtime, strftime
from datetime import datetime

#
# MongoDB read-only connectivity
#
mongo_uri = os.getenv('MONGO_URI')
mgo = MongoClient(mongo_uri)

#
# Cassandra connectivity assumes port 9042
#
cass_host = os.getenv('CASSANDRA_HOST')
cass_cluster = Cluster([cass_host], port=9042, protocol_version=4, load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='Solr'))
cass_session = cass_cluster.connect(keyspace='analytics')
cass_session.default_timeout = None

#
# Cassandra prepared statements
#
insert_page = """
    INSERT INTO analytics.content (
    host, path, network_account_id, updated, published,
    redirect_url, title, description, image_url, content_type,
    keywords,first_sentence, first_sentence_code, edited_title,
    edited_description, edited_image_url, edited_message,
    edited_tweet, twitter_image_url, has_twitter_card, description_erased,
    title_erased, message_erased, tweet_erased, evergreen, ignored,
    evicted)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
insert_page_stmt = cass_session.prepare(insert_page)
insert_page_stmt.consistency_level = ConsistencyLevel.LOCAL_ONE

pages = mgo.pagedb.pages
ignore_decode_opts = CodecOptions(unicode_decode_error_handler='ignore')
pages = pages.with_options(codec_options=ignore_decode_opts)

def iterate(cursor):
    read=0
    written=0
    for doc in cursor:
        read += 1
        if read % 1000 == 0:
            print('{} | {} / {}'.format(strftime("%Y-%m-%d %H:%M:%S",gmtime()), written, read))

        published = doc.get('d')
#        visited = doc.get('v')
        id = str(doc['_id'])
        host = id.split('/', 1)[0]
        path = '/' + id.split('/', 1)[1].replace("'", "''")
        network_account_id = ""
        updated = datetime.now()
        redirect_url = ""
        title = str(doc['t']) if 't' in doc else ""
        description = str(doc['dd']) if 'dd' in doc else ""
        image_url = str(doc['iu']) if 'iu' in doc else ""
        content_type = str(doc['ct']) if 'ct' in doc else ""
        keywords = str(doc['k']) if 'k' in doc else ""
#        first_sentence_prefix = str(doc['fsp']) if 'fsp' in doc else ""
        first_sentence = str(doc['fs']) if 'fs' in doc else ""
        first_sentence_code = str(doc['fse']) if 'fse' in doc else ""
        edited_title = str(doc['et']) if 'et' in doc else ""
        edited_description = str(doc['ed']) if 'ed' in doc else ""
        edited_image_url = str(doc['ei']) if 'ei' in doc else ""
        edited_message = str(doc['em']) if 'em' in doc else ""
        edited_tweet = str(doc['etw']) if 'etw' in doc else ""
        twitter_image_url = str(doc['tiu']) if 'tiu' in doc else ""
        has_twitter_card = doc['tc'] if 'tc' in doc else False
        description_erased = doc['de'] if 'de' in doc else False
        title_erased = doc['te'] if 'te' in doc else False
        message_erased = doc['me'] if 'me' in doc else False
        tweet_erased = doc['twe'] if 'twe' in doc else False
        evergreen = doc['eg'] if 'eg' in doc else False
        ignored = doc['i'] if 'i' in doc else False
        evicted = False
#        scraped = doc['r'] if 'r' in doc else False


        bound = insert_page_stmt.bind((
            host, path, network_account_id, updated, published,
            redirect_url, title, description, image_url, content_type,
            keywords, first_sentence, first_sentence_code, edited_title,
            edited_description, edited_image_url, edited_message,
            edited_tweet, twitter_image_url, has_twitter_card, description_erased,
            title_erased, message_erased, tweet_erased, evergreen, ignored,
            evicted))

        cass_session.execute(bound)

        written += 1


try:
    cursor = pages.find(no_cursor_timeout=True)
    iterate(cursor)
finally:
    cursor.close()
    mgo.close()
    print('finished.')
