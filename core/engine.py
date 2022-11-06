
from core import config
from core.config import ConfiguredSource

import logging
from datetime import date

logger = logging.getLogger(__name__)


def run(begin: date, end: date) :
	logger.info("Working on the time period from %s to %s", begin, end)
	sources = config.load()
	if len(sources) == 0 :
		logger.warning('No sources found, exitting')
		return
	for src in sources :
		try :
			__b_processSource(src, begin, end)
		except Exception as e :
			for notifier in src.notifiers :
				notifier.notifyError(e)
			

def __b_processSource(src: ConfiguredSource, begin: date, end: date) :
	entries = src.source.getEntries(begin, end)
	filtered = [
		x for x in entries
		if x.title in src.list
	]
	# TODO database check
	info = src.source.getInfo()
	for entry in filtered :
		src.source.refineEntry(entry)
		for notifier in src.notifiers :
			notifier.notifyRelease(entry, info)
