
import logging
import sqlite3

logger = logging.getLogger(__name__)


class SqliteConnection :
	
	def __init__(self, path: str, autocommit = False) :
		self.path = path
		self.autocommit = autocommit
	
	def commit(self) :
		logger.debug('Committed on SQLite connection')
		self.con.commit()
	
	def cursor(self) -> sqlite3.Cursor :
		return self.con.cursor()
	
	def __enter__(self) -> "SqliteConnection" :
		self.con = sqlite3.connect(self.path)
		self.con.set_trace_callback(lambda s: logger.debug(s))
		logger.debug("Initiated SQLite connection to %s", self.path)
		return self

	def __exit__(self, exc_type, exc_value, traceback) :
		if self.autocommit and exc_type is None :
			self.commit()
		self.con.close()
		logger.debug("Closed SQLite connection to %s", self.path)
		return False
