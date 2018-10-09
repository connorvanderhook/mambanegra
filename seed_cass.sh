#!/usr/bin/env bash

set -o nounset
set -o errexit

echo '==> loading Cassandra schemas'
docker exec -i devenv_cassandra_1 cqlsh < ./experiment.cql
sleep 1