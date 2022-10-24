from elasticsearch import Elasticsearch
import indeces_schema as schema
import sys
from uuid import uuid4


class Indeces_Management:
    def __init__(self) -> None:
        self.es = Elasticsearch(schema.es_url)
        #後ほどパスワード設定しておく

        if not self.es.indices.exists(index=schema.index_name):
            #インデックスが構築されていないのでシステム停止する
            sys.exit(0)

    def regist_content(self):
        
        content_id = str(uuid4())
        
        
        self.es.create(index=schema.index_name, id=content_id)

    