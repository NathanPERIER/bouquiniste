
from core import config
from core.config import ConfiguredSource
from database import initDatabase, getDatabaseConnection
import database.queries

import logging
from datetime import date
from sqlite3 import Cursor

logger = logging.getLogger(__name__)


def run(begin: date, end: date) :
	logger.info("Working on the time period from %s to %s", begin, end)
	sources = config.load()
	if len(sources) == 0 :
		logger.warning('No sources found, exitting')
		return
	with getDatabaseConnection() as con :
		cur = con.cursor()
		initDatabase(cur)
		for src in sources :
			try :
				__b_processSource(src, begin, end, cur)
			except Exception as e :
				logger.exception("Uncaught error during source processing")
				for notifier in src.notifiers :
					notifier.notifyError(e)
			

def __b_processSource(src: ConfiguredSource, begin: date, end: date, cur: Cursor) :
	entries = src.source.getEntries(begin, end)
	filtered = [
		x for x in entries
		if x.title in src.names
		or x.manga_id in src.ids
	]
	filtered = database.queries.filterRecordedEntries(cur, src.identifier, filtered)
	info = src.source.getInfo()
	for entry in filtered :
		src.source.refineEntry(entry)
		for notifier in src.notifiers :
			notifier.notifyRelease(entry, info)
		database.queries.recordEntry(cur, src.identifier, entry)
