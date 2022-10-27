

index_name = "headlessfaq_content"

#contentID == elasticsearch document id
settings = {
    "number_of_shards": 2,
    "number_of_replicas": 1
}
mapping = {
    "dynamic":"true",
    "numeric_detection": "true",
    "properties": {
        "update_date": {"type": "date", "format": "yyyy-MM-dd"},
        "regist_user": {"type": "text"},
        "category": {"type": "text"},
        "question": {"type": "text"},
        "answer": {"type":"text"}
    }    
}

es_url = "http://localhost:9200"