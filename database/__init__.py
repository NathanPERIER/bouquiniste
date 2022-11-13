
from database.creation import create as initDatabase
from database.connection import SqliteConnection
from utils.paths import DATABASE_FILE as __DATABASE_FILE


def getDatabaseConnection() -> SqliteConnection :
	return SqliteConnection(__DATABASE_FILE, True)
