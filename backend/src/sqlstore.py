"""MariaDB-backed note storage — same interface as NoteStore (add/all/get/delete).

One connection per worker process; ping(reconnect=True) before each
operation so a database restart heals itself.
"""
import os
import pymysql


class SqlStore:
    def __init__(self) -> None:
        # establishes a connection object to MariaDB and keeps that
        # connection in self._conn.
        self._conn = pymysql.connect(
            host=os.environ.get("DB_HOST", "db"),
            user=os.environ.get("DB_USER", "notes"),
            password=os.environ.get("DB_PASSWORD", ""),
            database=os.environ.get("DB_NAME", "notes"),
            autocommit=True,
)

    def _db(self):
        # check if connection is broken due to Mariadb restaring
        # if it is, attempt to reconnect
        self._conn.ping(reconnect=True)
        return self._conn

    def add(self, title: str, body: str) -> dict:
        # curosr is an object that Executes SQL and retrieves results
        # use a with block to close cursor after return or incase of an
        # execute() crash
        with self._db().cursor() as cur:
            cur.execute(
                "INSERT INTO notes (title, body) Values (%s, %s)",
                (title, body)
                )
            # lastrowid because MariaDB automatically generates an ID when you
            # insert a note (id INT AUTO_INCREMENT PRIMARY KEY), gives the
            # recent one.
            return {"id": cur.lastrowid, "title": title, "body": body}

    def all(self) -> list[dict]:
        note_lst = []
        with self._db().cursor() as cur:
            cur.execute("SELECT id, title, body FROM notes ORDER BY id")
            for r in cur.fetchall():
                # r is a tuple
                note_lst.append({"id": r[0], "title": r[1], "body": r[2]})
        return note_lst

    def get(self, note_id: int) -> dict | None:
        with self._db().cursor() as cur:
            cur.execute(
                "SELECT id, title, body FROM notes WHERE id = %s",
                (note_id,))
            row = cur.fetchone()
            if row is None:
                return None
            return {"id": row[0], "title": row[1], "body": row[2]}

    def delete(self, note_id: int) -> bool:
        with self._db().cursor() as cur:
            cur.execute(
                "DELETE FROM notes WHERE id = %s",
                (note_id,))
            if cur.rowcount > 0:
                # if the note existed and was deleted then rowcount = 1
                return True
            else:
                return False
            
