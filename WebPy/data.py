import json
import sqlite3
from typing import Any

class DataBase:
    def __init__(self,table_name):
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        self.table_name = table_name
        self.table_name = ''.join(e for e in self.table_name if e.isalnum())
        self.c.execute('''CREATE TABLE IF NOT EXISTS {} (filename text,name text ,x text, y text, dx text, dy text, ocr text)'''.format(self.table_name))
        self.conn.commit()
    def select(self):
        self.c.execute("SELECT * FROM {}".format(self.table_name))
        return self.c.fetchall()
    def insert(self, filename: str, data: str):
        #data是一个一维json字符串,根据json中的关键字删除旧表，重新插入新表
        self.c.execute("DELETE FROM {}".format(self.table_name))
        json_data = json.loads(data)
        for key in json_data:
            if(key['ocr'] == ''):
                key['ocr'] = 'None'
            self.c.execute("INSERT INTO {} VALUES ('{}','{}','{}', '{}', '{}', '{}', '{}')".format(self.table_name, filename,key['name'] ,key['x'], key['y'], key['dx'], key['dy'], key['ocr']))
        self.conn.commit()

    def close(self):
        self.conn.close()