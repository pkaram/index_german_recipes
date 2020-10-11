# Create Index on Elasticsearch 

In this repo the test dataset https://www.kaggle.com/sterby/german-recipes-dataset 
on German Recipes was used to create with Python an Index on Elasticsearch.

Elasticsearch should be up an running on localhost:9200 before the script is executed.

User should download the data from the link and place them in the same folder with 
the scripts included. By executing the following on command line

```
python create_elasticsearch_index.py
```

the user will create a 'recipe_index' which will include various information for
further of a set of recipes. 

As an example to query the index for all recipes which are have *Rindfleisch* as an ingredient 
execute on python console: 
```
from elasticsearch import Elasticsearch
es = Elasticsearch(host="localhost", port=9200)
res=es.search(index='recipe_index',body={'query':{"match":{'Ingredients_unique':'Rindfleisch'}}})
```
