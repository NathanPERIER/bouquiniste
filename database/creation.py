
from sqlite3 import Cursor


def init(cur: Cursor) :
	cur.execute("""
CREATE TABLE IF NOT EXISTS notified (
	source_id TEXT NOT NULL,
	manga_id TEXT NOT NULL,
	entry_num INTEGER,
	date INTEGER NOT NULL,
	PRIMARY KEY (source_id, manga_id, entry_num)
);
	""")
	_ = cur.fetchone()

	cur.execute("""
CREATE TABLE IF NOT EXISTS following (
	source_id TEXT NOT NULL,
	series_id TEXT NOT NULL,
	PRIMARY KEY (source_id, series_id)
);
	""")
	_ = cur.fetchone()
