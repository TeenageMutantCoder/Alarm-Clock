import sqlite3


class SqlConnector():
    def __init__(self):
        self.conn = sqlite3.connect('alarms.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS alarms (primary_key INTEGER PRIMARY KEY, time_ TEXT NOT NULL, active INTEGER NOT NULL)")

    def collect(self):
        self.c.execute("SELECT * FROM alarms ORDER BY time_")
        return(self.c.fetchall())

    def read(self):
        self.c.execute("SELECT * FROM alarms ORDER BY time_")
        data = self.c.fetchall()
        for row in data:
            print(row)

    def insert(self, time, active):
        self.c.execute("INSERT INTO alarms(time_, active) VALUES (?, ?)", 
                       (time, active))
        self.commit()

    def edit(self, initial_time, new_time, active):
        self.c.execute("UPDATE alarms SET time_=?, active=? WHERE time_=?", 
                       (new_time, active, initial_time))
        self.commit()

    def delete(self, key):
        self.c.execute("DELETE FROM alarms WHERE primary_key=?", (key,))
        self.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
    
    def _empty(self):
        self.c.execute("DELETE FROM alarms")
        self.commit()

if __name__ == "__main__":
    db = SqlConnector()
    db.read()
    db.close()