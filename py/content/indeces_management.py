
from elasticsearch import Elasticsearch
from .indeces_schema import es_url, index_name
import sys
from .content_schema import Content
from typing import List

class Indeces_Management:
    """
    ElasticSearchに向けてIndexの管理を行うクラス
    """
    def __init__(self) -> None:
        self.es = Elasticsearch(es_url)
        #後ほどパスワード設定しておく
        if not self.es.indices.exists(index=index_name):
            #インデックスが構築されていないのでシステム停止する
            sys.exit(0)
        

class Content_Management(Indeces_Management):
    """
    ElasticSearchに向けてコンテンツの管理を行うクラス

    """
    def __init__(self) -> None:
        super().__init__()
    
    def create_content(self, body:Content):
        """コンテンツを登録"""
        result = self.es.create(
            index=index_name, 
            id=body.content_id, 
            document=body.to_content()
        )

        if result["result"] != "created":
            #返却内容のkey=>resultがcreatedでない場合、おかしい
            raise Content_Managment_Error("failed regist content to elastisearch")
        #{'_index': 'headlessfaq_content', '_id': 'bda45033-ba78-4408-a02e-f426d1873493', '_version': 1, 'result': 'created', '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 0, '_primary_term': 1}
    
    def update_content(self, body:Content):
        """コンテンツを更新"""
        result = self.es.update(
            index=index_name, 
            id=body.content_id, 
            doc=body.to_new_content()
        )

        if result["result"] != "updated":
            raise Content_Managment_Error(f"failed update content:{body.content_id}")

    def get_content(self, id:str)->Content:
        """
        コンテンツをIDをもとに取得してくる
        Parameter: 
            id : str elasticsearch のdocument id 
        Return:
            Content: idでヒットしたFAQ
        """
        result = self.es.get(index=index_name, id=id)
        if "_source" in result:
            content = Content()
            content.set_content(result)
            return content
        else:
            raise Content_Managment_Error(f"faild get content from id={id}")
            
    def search_content(self, body:Content, size:int=5)->List[Content]:
        """コンテンツを検索"""
        result = self.es.search(
            index=index_name, 
            query=body.to_query(), 
            size=size
        )
        contents = []
        for content in result["hits"]["hits"]:
            faq = Content()
            faq.set_content(content)
            contents.append(faq)
        return contents

    def count_content(self)->int:
        """現在のインデックスに登録されているコンテンツの数をカウントする"""
        result = self.es.count(index=index_name)
        count = result.get("count")
        if count is None:
            raise Content_Managment_Error("failed count content from index")

    def delete_content(self, body:Content):
        self.es.delete(
            index=index_name, 
            id=body.content_id,
            ignore=[404] #存在しないidの場合は無視する
        )

        if self.es.exists(index=index_name, id=body.content_id):
            #trueの場合消えてないということなので、おかしい
            raise Content_Managment_Error("faild delete content")

    def groupby_category_content_count(self)->dict:
        """
        カテゴリーごとのコンテンツ数を取得する関数
        """
        result = self.es.search(
            index=index_name, 
            aggs={
                "group_by_category": {
                    "terms": {
                        "field": "doc.category.keyword",
                        "size":1000
                    }
                }
            },
            size = 0
        )
        category_count_dict = { category["key"]: category["doc_count"] 
            for category in result["aggregations"]["group_by_category"]["buckets"] }
        return category_count_dict
    
    def get_all_category(self)->list:
        """
        groupby_category_content_count関数を用いて,カテゴリー一覧を取得する
        """
        category_dict = self.groupby_category_content_count()
        return list(category_dict.keys())

        
class Content_Managment_Error(Exception):
    pass
    