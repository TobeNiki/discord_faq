import time
import uuid

class Content:
    def __init__(self) -> None:
        self.content_id  = str(uuid.uuid4())
        self.update_date = time.time()
        self.regist_user = ""
        self.category    = ""
        self.question    = ""
        self.answer      = ""

    
    def to_content(self) -> dict:
        content = {
            "update_date" : self.update_date,
            "regist_user" : self.regist_user,
            "category"    : self.category, 
            "question"    : self.question,
            "answer"      : self.answer
        }
        return content