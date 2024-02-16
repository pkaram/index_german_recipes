# Create Index on Elasticsearch 

In this repo the test dataset https://www.kaggle.com/sterby/german-recipes-dataset 
on German Recipes was used to create with Python an Index on Elasticsearch.

1. Start Elasticsearch and Kibana with docker compose:

```
docker-compose up --build -d
```

2. Setup the environment with conda:

```
conda create -n igr python=3.10 -y
conda activate igr
pip install -r requirements.txt
```
3. [Modify username/key](kaggle.json):

```
{"username":"yourusername","key":"yourkey"}
```

4. Make sure that Elasticsearch is up and running and index the documents with the following:

```
python src/main.py
```

A *german_recipes* index will be created. You can use Kibana for search directly on http://localhost:5601/.
