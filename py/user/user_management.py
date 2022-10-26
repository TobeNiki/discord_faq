
import hashlib
import sqlite3

db_name = "./headless_faq.db"

class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(db_name, isolation_level='DEFERRED')

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute("CREATE TABLE user(name TEXt PRIMARY KEY, password TEXT)")
        self.conn.commit()
        self.conn.close()

class User_Managemtn(Database):
    def __init__(self) -> None:
        super().__init__()

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
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO user(name, password) values(?, ?)", [name, hashed_password])
            self.conn.commit()
        except Exception:
            self.conn.rollback()
    
        cur.close()

    def delete_user (self, name:str, password:str):
        """
        ユーザの削除：
        """
        hashed_password = self.password2hash(password=password)
        try:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM user WHERE name = ? AND password = ?", [name, hashed_password])
            self.conn.commit()
        except Exception:
            self.conn.rollback()
        
        cur.close()


if __name__ == "__main__":
    db = Database()
    db.create_table()