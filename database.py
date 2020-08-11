import sqlite3

class database:
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.curs = self.connection.cursor()
        self.curs.execute(
            "CREATE TABLE IF NOT EXISTS target (id INTEGER PRIMARY KEY, target text, date text, condition text)")
        self.connection.commit()
    
    def fetch(self):
        self.curs.execute("SELECT * FROM target")
        rows = self.curs.fetchall()
        return rows
    
    def insert(self, target, date, condition):
        self.curs.execute("INSERT INTO target VALUES (NULL, ?, ?, ?)",
                            (target, date, condition))
        self.connection.commit()
    
    def remove(self, id):
        self.curs.execute("DELETE FROM target WHERE id=?", (id,))
        self.connection.commit()
    
    def update(self, id, target, date, condition):
        self.curs.execute("UPDATE target SET target = ?, date = ?, condition = ? WHERE id = ?", (target ,date, condition, id) )
        self.connection.commit()
    