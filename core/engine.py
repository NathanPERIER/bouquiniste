
from core import config
from core.config import ConfiguredSource
from utils.exceptions import BadConfigException
from database import getDatabaseConnection
import database
import database.queries

import logging
from datetime import date
from sqlite3 import Cursor

logger = logging.getLogger(__name__)


def init() :
	config.init()
	with getDatabaseConnection() as con :
		cur = con.cursor()
		database.init(cur)


def run(begin: date, end: date) :
	logger.info("Working on the time period from %s to %s", begin, end)
	with getDatabaseConnection() as con :
		cur = con.cursor()
		sources = config.load(cur)
		if len(sources) == 0 :
			logger.warning('No sources found, exitting')
			return
		for src in sources.values() :
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
		if x.manga_id in src.ids
	]
	filtered = database.queries.filterRecordedEntries(cur, src.identifier, filtered)
	info = src.source.getInfo()
	for entry in filtered :
		src.source.refineEntry(entry)
		for notifier in src.notifiers :
			notifier.notifyRelease(entry, info)
		database.queries.recordEntry(cur, src.identifier, entry)


def followSeries(source_id: str, url: str) :
	with getDatabaseConnection(False) as con :
		cur = con.cursor()
		sources = config.load(cur)
		if source_id not in sources :
			raise BadConfigException(f"Source {source_id} not found")
		cs = sources[source_id]
		series_id = cs.source.getSeriesId(url)
		if series_id is None :
			raise ValueError(f"URL {url} is not associated with a series from source {source_id}")
		if database.queries.followSeries(cur, source_id, series_id) :
			con.commit()
