import os
import uuid
import binascii as bda
from time import gmtime, strftime
from bson import CodecOptions
from pymongo import MongoClient
from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
# from .analysis_dictionary import ANALYSIS_DICT

ANALYSIS_DICT = {
    # Current Production ('tademo.trueanthem.com/this/is/your/article/speaking-1')
    0: {"id": "ranked.current",
        "f": lambda x, y, z, v: x+y,
        "l": "Current Production",
        "t": "token(host, path)"},
    # Reversed PageID ('1-gnikaeps/elcitra/ruoy/si/siht/moc.mehtnaeurt.omedat')
    1: {"id": "ranked.uno",
        "f": lambda x, y, z, v: x + y[::-1],
        "l": "Reversed PageID",
        "t": "token(key)"},
    # CRC32 of PageID: ('2224592772')
    2: {"id": "ranked.dos",
        "f": lambda x, y, z, v:
        str(bda.crc32(bytes(x + y, 'UTF-8')) & 0xffffffff),
        "l": "CRC32 of PageID",
        "t": "token(key, host)"},
    # Path + Host ('/this/is/your/article/speaking-1tademo.trueanthem.com')
    3: {"id": "ranked.tres",
        "f": lambda x, y, z, v: y + x,
        "l": "Path + Host",
        "t": "token(path, host)"},
    # CRC32(Path) + Host ('2894818572tademo.trueanthem.com')
    4: {"id": "ranked.cuatro",
        "f": lambda x, y, z, v:
            str(bda.crc32(bytes(y, 'UTF-8')) & 0xffffffff) + x,
        "l": "CRC32(Path) + Host",
        "t": "token(key)"},
    5: {"id": "ranked.seis",
        "f": lambda x, y, z, v: z + x,
        "l": "YYYY-MM-DD + Host",
        "t": "token(day, host)"},
    6: {"id": "ranked.siete",
        "f": lambda x, y, z, v: z + x + y,
        "l": "YYYY-MM-DD + Host + Path",
        "t": "token(day, host, path)"},
    7: {"id": "ranked.ocho",
        "f": lambda x, y, z, v: v + x,
        "l": "YYYY-MM + Host",
        "t": "token(month, host)"},
}

#
# MongoDB read-only connectivity
#
mongo_uri = os.getenv('MONGO_URI')
mgo = MongoClient(mongo_uri)
pages = mgo.pagedb.pages
ignore_decode_opts = CodecOptions(unicode_decode_error_handler='ignore')
pages = pages.with_options(codec_options=ignore_decode_opts)


#
# Cassandra connectivity assumes port 9042
#
cass_host = os.getenv('CASSANDRA_HOST')
cass_cluster = Cluster([cass_host], port=9042, protocol_version=4)
cass_session = cass_cluster.connect(keyspace='ranked')
cass_session.default_timeout = None


def generate_insert_statement(table_name):
    """
    Cassandra insert statement using the table_name
    :param table_name: table name denotes which table to create the record
    """
    insert_statement = "INSERT INTO " + \
                       table_name + \
                       "(host, path, key, published, day, month) " \
                       "VALUES (?, ?, ?, ?, ?, ?)"
    prepared_insert_stmt = cass_session.prepare(insert_statement)
    prepared_insert_stmt.consistency_level = ConsistencyLevel.LOCAL_ONE
    return prepared_insert_stmt


def insert_page(table_name, doc, key):
    """
    Generate the insert statement using table_name &
    Execute cassandra insert binding doc and key
    :param doc: page document (contains fields: id, host, path, published)
    :param key: the key generated from the dictionary of algorithms
    :param table_name: table to insert the new page
    """
    insert_stmt = generate_insert_statement(table_name)
    bound = insert_stmt.bind((
        doc['host'], doc['path'], key, doc['published'], doc['day'], doc['month']
    ))
    cass_session.execute(bound)


def key_generator(i, host, path, day, month):
    """ key_generator uses the dictionary of key algorithms
        to lookup the iteration and return the lambda function
        that will create key and the table that it will insert to.
    """
    try:
        return ANALYSIS_DICT[i]["f"](host, path, day, month), ANALYSIS_DICT[i]["id"]
    except Exception as err:
        print('help', err)
    return '', ''


def iterate(cursor):
    """
    iterate over the returned results from mongodb
    :param cursor: mongodb page documents returned from query
    """
    read=0
    written=0
    for doc in cursor:
        if read % 1000 == 0:
            print('{} | {} / {}'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime()), written, read))

        new_doc = dict()
        new_doc['published'] = doc['d']
        new_doc['day'] = str(doc['d'])[0:10]
        new_doc['month'] = str(doc['d'])[0:7]
        new_doc['id'] = str(doc['_id'])
        new_doc['host'] = new_doc['id'].split('/', 1)[0]
        new_doc['path'] = '/' + new_doc['id'].split('/', 1)[1].replace("'", "''")

        for x in range(0, len(ANALYSIS_DICT)):
            try:
                k, t = key_generator(x,
                                     new_doc['host'],
                                     new_doc['path'],
                                     new_doc['day'],
                                     new_doc['month'])
                insert_page(t, new_doc, k)
                written += 1
            except TypeError as err:
                print(err)

        read += 1


try:
    cursor = pages.find({}, no_cursor_timeout=True)
    iterate(cursor)
finally:
    cursor.close()
    mgo.close()
    print('finished.')