import codecs
import csv
import os
import logging
import binascii
# import matplotlib.pyplot as plt
# from google.cloud import storage
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
# from mambanegra.analysis_dictionary import ANALYSIS_DICT
# from .google_storage import blob_name, CatalogBlob, apply_settings

ANALYSIS_DICT_2 = {
    # Current Production ('tademo.trueanthem.com/this/is/your/article/speaking-1')
    0: {"id": "ranked.current",
        "f": lambda x, y, z, v: x+y,
        "l": "Current Production",
        "t": "token(host, path)",
        "fn":"production.csv"},
    # Reversed PageID ('1-gnikaeps/elcitra/ruoy/si/siht/moc.mehtnaeurt.omedat')
    1: {"id": "ranked.uno",
        "f": lambda x, y, z, v: x+y[::-1],
        "l": "Reversed PageID",
        "t": "token(key)",
        "fn":"reversed_page_id.csv"},
# CRC32 of PageID: ('2224592772')
    2: {"id": "ranked.dos",
        "f": lambda x, y, z, v: str(binascii.crc32(bytes(x+y, 'UTF-8')) & 0xffffffff),
        "l": "CRC32 of PageID",
        "t": "token(key, host)",
        "fn":"crc32_page_id.csv"},
    # Path + Host ('/this/is/your/article/speaking-1tademo.trueanthem.com')
    3: {"id": "ranked.tres",
        "f": lambda x, y, z, v: y+x,
        "l": "Path + Host",
        "t": "token(path, host)",
        "fn":"path_host.csv"},
    # CRC32(Path) + Host ('2894818572tademo.trueanthem.com')
    4: {"id": "ranked.cuatro",
        "f": lambda x, y, z, v: str(binascii.crc32(bytes(y, 'UTF-8')) & 0xffffffff)+x,
        "l": "CRC32(Path) + Host",
        "t": "token(key)",
        "fn":"crc32path_host.csv"},
    5: {"id": "ranked.seis",
        "f": lambda x, y, z, v: z+x,
        "l": "YYYY-MM-DD + Host",
        "t": "token(day, host)",
        "fn":"yyyy-mm-dd_host.csv"},
    6: {"id": "ranked.siete",
        "f": lambda x, y, z, v: z+x+y,
        "l": "YYYY-MM-DD + Host + Path",
        "t": "token(day, host, path)",
        "fn":"yyyy-mm-dd_host_path.csv"},
    7: {"id": "ranked.ocho",
        "f": lambda x, y, z, v: v+x,
        "l": "YYYY-MM + Host",
        "t": "token(month, host)",
        "fn":"yyyy-mm_host.csv"},
}

_CacheLevel = 'no-cache'
_PLOT_TYPE = os.getenv('PLOT_TYPE')
_CASSANDRA_HOST = os.getenv('CASSANDRA_HOST')
_BIN_COUNT = os.getenv('BIN_COUNT')


#
# Cassandra connectivity assumes port 9042
#
cass_cluster = Cluster([_CASSANDRA_HOST], port=9042, protocol_version=4)
cass_session = cass_cluster.connect(keyspace='ranked')
cass_session.row_factory = dict_factory


def generate_select_statement(token_val, table_name):
    """
    Cassandra select statement using the table_name
    :param table_name: table name denotes which table to select the records
    """
    select_statement = "SELECT host, path, key, month, day, " + token_val + " FROM " + table_name
    prepared_select_stmt = cass_session.prepare(select_statement)
    prepared_select_stmt.consistency_level = ConsistencyLevel.LOCAL_ONE
    return prepared_select_stmt


def query_pages(table_name, key):
    """
    Generate the select statement using table_name &
    Execute the query to cassandra
    :param key: the key generated from the dictionary of algorithms
    :param table_name: table to insert the new page
    """
    select_stmt = generate_select_statement(key, table_name)
    try:
        return cass_session.execute_async(select_stmt)
    except BaseException as err:
        print('houston has problems', err)
    return None


def product_keys(token_val):
    return ["host", "path", "key", token_val, "month", "day", "published"]
# -
#  day       | 2017-11-10
#  host      | www.bestproducts.com
#  path      | /lifestyle/g1651/innovative-kickstarter-campaigns/
#  key       | 2017-11-10www.bestproducts.com/lifestyle/g1651/innovative-kickstarter-campaigns/
#  month     | 2017-11
#  published | 2017-11-10 09:00:00.000000+0000
#  uuid      | null


# def main():
"""
Export catalog feed from postgres and upload to Google Cloud Storage bucket.
Convert the catalog product price from the cents value stored in the db
back to a dollar amount.
"""
for x in range(0, len(ANALYSIS_DICT_2)):
    print('loop ', x)
    table = ANALYSIS_DICT_2[x]['id']
    token = ANALYSIS_DICT_2[x]['t']
    label = ANALYSIS_DICT_2[x]['l']
    token_val = 'system.' + token
    with codecs.open(ANALYSIS_DICT_2[x]['fn'], 'w+', encoding='utf-8-sig') as csv_file:
        writer = csv.DictWriter(csv_file,
                                fieldnames=product_keys(token_val),
                                extrasaction='ignore')
        writer.writeheader()
        data = []
        s = 0

        future = query_pages(table, token)
        try:
            rows = future.result()
            if rows is not None:
                for row in rows:
                    s = s + 1
                    # data.append(row['system.' + token])
                    writer.writerow(row)

                ###  NOT NEEDED for Data Export
                # a = np.vstack(data)
                # x, y, z = make_plot(a, label)
                # print('> {} | Min:{} | Max:{} | Range:{} | Mean:{} | Std:{}'.format(
                #     label,
                #     min(x),
                #     max(x),
                #     float(max(x) - min(x)),
                #     np.mean(x),
                #     np.std(x)))
                ###

        except TypeError as err:
            print("Query timed out: ", err)

#
# plt.xlabel("Token Range")
# plt.ylabel("Records out of " + str(s))
# low = round(max(x)*0.99)
# high = round(max(x)*1.01)
# plt.ylim(low, high)
# plt.grid(True)
# plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05),
#            ncol=3, fancybox=True, shadow=True)
# plt.show()