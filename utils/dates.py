
from datetime import datetime, date

LOG_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

def dateToTimestamp(d: date) -> float :
	dt = datetime.combine(d, datetime.min.time())
	return dt.timestamp()