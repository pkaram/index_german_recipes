import process_data
from elasticsearch import Elasticsearch,helpers

#load data
recipes,ingredients_df=process_data.main()

#elasticsearch should be up and running on localhost:9200
es = Elasticsearch(host="localhost", port=9200)

actions = [{
            "_index":"recipe_index",
            "_id": recipes_dict['id'][i],
            "Url": recipes_dict['Url'][i],
            "Instructions": recipes_dict['Instructions'][i],
            "Ingredients": recipes_dict['Ingredients'][i],
            "Ingredients_unique":ingredients_df[ingredients_df.id == recipes_dict['id'][i]].ingredient.values.tolist(),
            "Name": recipes_dict['Name'][i]
        }
for i in range(0, len(recipes_dict['Url'].keys()))
]

#bulk insert to index
helpers.bulk(es,actions)

#view the data
#localhost:9200/recipe_index/_search?pretty