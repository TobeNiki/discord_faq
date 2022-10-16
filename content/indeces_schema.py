
index_name = "headlessfaq_content"

#contentID == elasticsearch document id
mapping = {
    "mappings": {
        "properties": {
            "update_date": {"type": "date", "format": "yyyy-MM-dd"},
            "regist_user": {"type": "text"},
            "category": {"type": "text"},
            "question": {"type": "text"},
            "answer": {"type":"text"}
        }
    }
}

es_url = "http://localhost:9200"

if __name__ == "__main__":

    from elasticsearch import Elasticsearch
    es = Elasticsearch(es_url)
    es.indices.create(index=index_name, body=mapping)

