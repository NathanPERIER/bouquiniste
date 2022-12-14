
from core.models import ReleaseEntry

import logging
from typing import Sequence
from sqlite3 import Cursor
from datetime import datetime

logger = logging.getLogger(__name__)


def filterRecordedEntries(cur: Cursor, source_id: str, entries: Sequence[ReleaseEntry]) -> Sequence[ReleaseEntry] :
	recorded = []
	for e in entries :
		cur.execute(
			'SELECT COUNT(*) FROM notified WHERE source_id=? AND manga_id=? AND entry_num=?;', 
			(source_id, e.manga_id, e.number)
		)
		recorded.append(cur.fetchone())
	return [e for e, rec in zip(entries, recorded) if rec[0] == 0]


def recordEntry(cur: Cursor, source_id: str, entry: ReleaseEntry) :
	timestamp = int(datetime.now().timestamp())
	values = (source_id, entry.manga_id, entry.number, timestamp)
	logger.debug("Registered notified entry %s", str(values))
	cur.execute('INSERT INTO notified VALUES(?, ?, ?, ?);', values)
	_ = cur.fetchone()


def followSeries(cur: Cursor, source_id: str, series_id: str) -> bool :
	values = (source_id, series_id)
	cur.execute('SELECT COUNT(*) FROM following WHERE source_id=? AND series_id=?;', values)
	modified = (cur.fetchone()[0] == 0)
	if modified :
		cur.execute('INSERT INTO following VALUES(?, ?);', values)
		_ = cur.fetchone()
	return modified


def getFollowedSeries(cur: Cursor, source_id: str) -> Sequence[str] :
	values = (source_id,)
	cur.execute('SELECT series_id FROM following WHERE source_id=?;', values)
	return [x[0] for x in cur.fetchall()]
