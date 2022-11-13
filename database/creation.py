
from sqlite3 import Cursor


def create(cur: Cursor) :
	cur.execute("""
CREATE TABLE IF NOT EXISTS notified (
	source_id TEXT NOT NULL,
	manga_id TEXT NOT NULL,
	entry_num INTEGER,
	date INTEGER NOT NULL,
	PRIMARY KEY (source_id, manga_id, entry_num)
);
	""")
