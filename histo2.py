# from matplotlib import colors
import matplotlib.pyplot as plt
# import logging
import numpy as np
from cassandra import ConsistencyLevel

# ReadTimeout
from cassandra.cluster import Cluster
from cassandra.query import dict_factory

#
# Cassandra connectivity assumes port 9042
#
cass_cluster = Cluster(['localhost'], port=9042, protocol_version=4)
cass_session = cass_cluster.connect(keyspace='ranked')
cass_session.row_factory = dict_factory


token_dictionary = {
    'ranked.current': 'token(host, path)',
    'ranked.uno': 'token(key)',
    'ranked.dos': 'token(key, host)',
    'ranked.tres': 'token(path, host)',
    'ranked.cuatro': 'token(key)'
}


def generate_select_statement(token_val, table_name):
    """
    Cassandra select statement using the table_name
    :param table_name: table name denotes which table to select the records
    """
    select_statement = "SELECT " + token_val + " FROM " + table_name
                       #
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


tables = [
    'ranked.current',
    'ranked.uno',
    'ranked.dos',
    'ranked.tres',
    'ranked.cuatro'
]


for t in tables:
    data = []
    s = 0
    token = token_dictionary[t]
    future = query_pages(t, token)
    try:
        rows = future.result()
        if rows is not None:
            for row in rows:
                s = s+1
                data[t].append(row['system.'+token])
                # a = np.vstack(data)
            # if t == 'ranked.current':
            #     plt.hist(data, bins=8, facecolor='b', stacked=True, histtype='step', normed=True, label='Current Production')
            # elif t == 'ranked.uno':
            #     plt.hist(data, bins=8, facecolor='g', stacked=True, histtype='step', normed=True, label='Reversed PageID')
            # elif t == 'ranked.dos':
            #     plt.hist(data, bins=8, facecolor='m', stacked=True, histtype='step', normed=True, label='CRC32 of PageID')
            # elif t == 'ranked.tres':
            #     plt.hist(data, bins=8, facecolor='c', stacked=True, histtype='step', normed=True, label='Path + Host')
            # elif t == 'ranked.cuatro':
            #     plt.hist(data, bins=8, facecolor='k', stacked=True, histtype='step', normed=True, label='CRC32(Path) + Host')

    except TypeError as err:
        print("Query timed out: ", err)


plt.hist(data, bins=8, facecolor='k', stacked=True, histtype='step', normed=True)
plt.xlabel("Token Range")
plt.ylabel("Records out of " + str(s))
plt.grid(True)
plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True)
plt.show()