
from content.indeces_schema import es_url,index_name, mapping, settings
if __name__ == "__main__":

    from elasticsearch import Elasticsearch
    es = Elasticsearch(es_url)
    es.indices.create(index=index_name, settings=settings, mappings=mapping)

