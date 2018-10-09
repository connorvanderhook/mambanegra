### La Mamba Negra
Un repositorio de python

## Develop

Once, you should set-up a virtual env on your Mac:

```bash
mkdir ~/Virtualenvs
cd ~/Virtualenvs
virtualenv -p python3 mambanegra
source ~/Virtualenvs/mambanegra/bin/activate
```

Each time you start your development session:

```bash
cd <your-path-to>/mambanegra
git submodule update --init
source ~/Virtualenvs/mambanegra/bin/activate
pip install -r requirements.txt
```

To shutdown
```
deactivate
```

`export MONGO_URI=localhost:27017`

`export CASSANDRA_HOST=localhost`