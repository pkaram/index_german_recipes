"script to perform etl from kaggle to elasticsearch"
import glob
import logging
from elasticsearch import Elasticsearch,helpers
from etl_utils import load_and_process, doc_generator, unzip_file, download_data

KAGGLE_DATASET = 'sterby/german-recipes-dataset'
INDEX_NAME = 'german_recipes'
logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    try:
        logging.info('processing data')
        download_data(KAGGLE_DATASET)
        zip_files = glob.glob("./data/*.zip")
        unzip_file(zip_files[0])
        json_files = glob.glob("./data/*.json")
        recipes = load_and_process(json_files[0])
    except Exception as e:
        logging.info('error while data etl: %s', e)
    es=Elasticsearch([{"host":"localhost","port":9200,"scheme":"http"}])
    index_exists = es.indices.exists(index=INDEX_NAME)
    if index_exists is False:
        logging.info('INDEX_NAME: %s does not exist and will be created', INDEX_NAME)
    docs = doc_generator(recipes, INDEX_NAME)
    helpers.bulk(es, docs)
    logging.info('data indexed')
