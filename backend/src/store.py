# in-memory note storage instaed of database, will be replaced by MariaDB in a
# later step, same interface.
# same interface means change functions implementation to execute SQL queries
# against MariaDB.
# But the rest of your application will continue calling the exact
# same functions.
class NoteStore():
    def __init__(self) -> None:
        self._notes: dict[int, dict] = {}
        self._next_id: int = 1

    def add(self, title: str, body: str) -> dict:
        note = {
            "id": self._next_id,
            "title": title,
            "body": body
        }
        self._notes[self._next_id] = note
        self._next_id += 1
        return note

    def all(self) -> list[dict]:
        # list because JSON arrays come from lists, not dicts
        # values so we get the notes without their ids, a list of dictionaries
        return list(self._notes.values())

    def get(self, note_id: int) -> dict | None:
        return self._notes.get(note_id, None)

    def delete(self, note_id: int) -> bool:
        deleted_note = self._notes.pop(note_id, None)
        if deleted_note is None:
            return False
        return True
