USE ranked;

CREATE TABLE IF NOT EXISTS ranked.current (
host text,
path text,
published timestamp,
key text,
uuid uuid,
day text,
month text,
PRIMARY KEY ((host, path))
) WITH compaction = { 'class': 'LeveledCompactionStrategy', 'tombstone_compaction_interval': '86400', 'sstable_size_in_mb': '160' , 'unchecked_tombstone_compaction': 'true' }
  AND compression = { 'sstable_compression' : 'LZ4Compressor' }
  AND gc_grace_seconds = 0;

CREATE TABLE IF NOT EXISTS ranked.uno (
host text,
path text,
published timestamp,
key text,
uuid uuid,
day text,
month text,
PRIMARY KEY ((key), host, path)
) WITH compaction = { 'class': 'LeveledCompactionStrategy', 'tombstone_compaction_interval': '86400', 'sstable_size_in_mb': '160' , 'unchecked_tombstone_compaction': 'true' }
  AND compression = { 'sstable_compression' : 'LZ4Compressor' }
  AND gc_grace_seconds = 0;

CREATE TABLE IF NOT EXISTS ranked.dos (
host text,
path text,
published timestamp,
key text,
uuid uuid,
day text,
month text,
PRIMARY KEY ((key, host), path)
) WITH compaction = { 'class': 'LeveledCompactionStrategy', 'tombstone_compaction_interval': '86400', 'sstable_size_in_mb': '160' , 'unchecked_tombstone_compaction': 'true' }
  AND compression = { 'sstable_compression' : 'LZ4Compressor' }
  AND gc_grace_seconds = 0;

CREATE TABLE IF NOT EXISTS ranked.tres (
host text,
path text,
published timestamp,
key text,
uuid uuid,
day text,
month text,
PRIMARY KEY ((path, host))
) WITH compaction = { 'class': 'LeveledCompactionStrategy', 'tombstone_compaction_interval': '86400', 'sstable_size_in_mb': '160' , 'unchecked_tombstone_compaction': 'true' }
  AND compression = { 'sstable_compression' : 'LZ4Compressor' }
  AND gc_grace_seconds = 0;


CREATE TABLE IF NOT EXISTS ranked.cuatro (
host text,
path text,
published timestamp,
key text,
uuid uuid,
day text,
month text,
PRIMARY KEY ((key), host)
) WITH compaction = { 'class': 'LeveledCompactionStrategy', 'tombstone_compaction_interval': '86400', 'sstable_size_in_mb': '160' , 'unchecked_tombstone_compaction': 'true' }
  AND compression = { 'sstable_compression' : 'LZ4Compressor' }
  AND gc_grace_seconds = 0;

CREATE TABLE IF NOT EXISTS ranked.cinco (
host text,
path text,
published timestamp,
key text,
uuid uuid,
day text,
month text,
PRIMARY KEY ((uuid), host, path)
) WITH compaction = { 'class': 'LeveledCompactionStrategy', 'tombstone_compaction_interval': '86400', 'sstable_size_in_mb': '160' , 'unchecked_tombstone_compaction': 'true' }
  AND compression = { 'sstable_compression' : 'LZ4Compressor' }
  AND gc_grace_seconds = 0;


CREATE TABLE IF NOT EXISTS ranked.seis (
host text,
path text,
published timestamp,
key text,
uuid uuid,
day text,
month text,
PRIMARY KEY ((day, host), path)
) WITH compaction = { 'class': 'LeveledCompactionStrategy', 'tombstone_compaction_interval': '86400', 'sstable_size_in_mb': '160' , 'unchecked_tombstone_compaction': 'true' }
  AND compression = { 'sstable_compression' : 'LZ4Compressor' }
  AND gc_grace_seconds = 0;

CREATE TABLE IF NOT EXISTS ranked.siete (
host text,
path text,
published timestamp,
key text,
uuid uuid,
day text,
month text,
PRIMARY KEY ((day, host, path))
) WITH compaction = { 'class': 'LeveledCompactionStrategy', 'tombstone_compaction_interval': '86400', 'sstable_size_in_mb': '160' , 'unchecked_tombstone_compaction': 'true' }
  AND compression = { 'sstable_compression' : 'LZ4Compressor' }
  AND gc_grace_seconds = 0;

CREATE TABLE IF NOT EXISTS ranked.ocho (
host text,
path text,
published timestamp,
key text,
uuid uuid,
day text,
month text,
PRIMARY KEY ((month, host), path)
) WITH compaction = { 'class': 'LeveledCompactionStrategy', 'tombstone_compaction_interval': '86400', 'sstable_size_in_mb': '160' , 'unchecked_tombstone_compaction': 'true' }
  AND compression = { 'sstable_compression' : 'LZ4Compressor' }
  AND gc_grace_seconds = 0;