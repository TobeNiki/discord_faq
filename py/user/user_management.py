
import hashlib
import sqlite3

db_name = "./headless_faq.db"


def create_table(self):
    cur = conn = sqlite3.connect(db_name)
    cur.execute("CREATE TABLE user(name TEXt PRIMARY KEY, password TEXT)")
    conn.commit()
    conn.close()

class User_Managemnt:
    def __init__(self) -> None:
        self.conn  = sqlite3.connect(db_name, isolation_level='DEFERRED')
    
    
    @staticmethod
    def password2hash(password:str)->str:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def basic_login (self, name:str, password:str)->bool:
        """
            ユーザ認証を行う:\n
            Parameter:
                name: str 名前 プライマリーキー
                password: str パスワード
            Return:
                bool ログインできたの判定bool値
            """
        cur = self.conn.cursor()
        hashed_password = self.password2hash(password)
        cur.execute("SELECT name FROM user WHERE password = ? AND name = ?", [hashed_password, name])
        result_list = cur.fetchall()

        return True if len(result_list) == 1 else False

    def regist_user (self, name:str, password:str):
        """
        ユーザの登録: \n
        """
        hashed_password = self.password2hash(password=password)
        is_failed_regist_user = False
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO user(name, password) values(?, ?)", [name, hashed_password])
            self.conn.commit()
        except Exception:
            is_failed_regist_user = True
            self.conn.rollback()
        cur.close()

        if is_failed_regist_user:
            raise User_Management_Error("failed regist user")

    def password_change(self, name:str, password:str):
        """ユーザのパスワード変更"""
        hashed_password = self.password2hash(password=password)
        is_failed_password_change = False
        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE user SET password = ? WHERE name", [hashed_password, name])
            self.conn.commit()
        except Exception:
            is_failed_password_change = True
            self.conn.rollback()
        
        cur.close()
        if is_failed_password_change:
            raise User_Management_Error("failed password change")

    def delete_user (self, name:str, password:str):
        """
        ユーザの削除：
        """
        hashed_password = self.password2hash(password=password)
        is_failed_delete_user = False
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM user WHERE name = ? AND password = ?", [name, hashed_password])
            self.conn.commit()
        except Exception:
            is_failed_delete_user = True
            self.conn.rollback()
        
        cur.close()
        if is_failed_delete_user:
            raise User_Management_Error("failed delete user")
class User_Management_Error(Exception):
    pass
