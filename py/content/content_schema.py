import datetime
import uuid


t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
def get_now_time()->str:
    """
    現在時刻を取得、フォーマットは"yyyy-MM-dd"
    """
    now = datetime.datetime.now(JST)
    return now.strftime('%Y-%m-%d')
    

class Content:
    def __init__(self, 
        content_id:str=None, 
        regist_user:str=None, 
        category:str=None, 
        question:str=None, 
        answer:str=None
        ) -> None:
        """
        FAQコンテンツの定義を行うクラス-elasticsearchに登録する内容と同じ
        Parameter:\n
            content_id: str default None: elasticsearchのドキュメントIDと同じ
            regist_user: str default None: FAQの登録者
            category: str FAQの分類を示す elasticsearchへの検索ではtermで一致するかの検索を行うfield
            question: str faqのタイトル=質問のこと elasticsearchへの検索では全文検索で行うfield
            answer: str faqの問いに対する答え
        """
        self.content_id  = content_id if content_id is not None else str(uuid.uuid4())
        self.update_date = get_now_time()
        self.regist_user = regist_user
        self.category    = category
        self.question    = question
        self.answer      = answer

    def to_query(self) -> dict :
        """
        Contentクラスのプロパティをもとにelasticsearch _searchにおけるqueryのJsonを発行する
        """
        match = {}
        term = {}
        if self.question != "" :
            match.setdefault("query", self.question)
            match.setdefault("operator", "and")
        
        if self.category != "":
            term.setdefault("category", self.category)
        
        if self.question != "" and self.category != "":
            return {"must": [{"match": { "question" : match } },{"term": term}]}
        
        elif self.question != "":
            return {"match": { "question" : match } }

        elif self.category != "":
            return { "term" : term }
            
        else:
            return { "match_all": {} }
            

    
    def to_new_content(self)->dict:
        content = { "update_date": self.update_date }
        
        if self.regist_user != "":
            content.setdefault("regist_user", self.regist_user)

        if self.category != "":
            content.setdefault("category",self.category)

        if self.question != "":
            content.setdefault("question", self.question)

        if self.answer != "":
            content.setdefault("answer", self.answer)

        return content 

    def to_content(self) -> dict:
        content = {
            "update_date" : self.update_date,
            "regist_user" : self.regist_user,
            "category"    : self.category, 
            "question"    : self.question,
            "answer"      : self.answer
        }
        return content
    
    def set_content(self, hits:dict):
        self.content_id = hits["_id"]
        source = hits["_source"]
        self.update_date = source["update_date"]
        self.regist_user = source["regist_user"]
        self.category = source["category"]
        self.question = source["question"]
        self.answer = source["answer"]