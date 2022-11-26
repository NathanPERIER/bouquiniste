
from database.creation import init
from database.connection import SqliteConnection
from utils.paths import DATABASE_FILE as __DATABASE_FILE


def getDatabaseConnection(autocommit = True) -> SqliteConnection :
	return SqliteConnection(__DATABASE_FILE, autocommit)
