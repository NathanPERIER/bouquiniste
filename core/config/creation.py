
from core.config.definitions import CONFIG_FOLDER, NOTIFIERS_FILE, SOURCES_FILE

import os
import logging

logger = logging.getLogger(__name__)

__all__ = [
	"init"
]


def init() :
	for folder in [CONFIG_FOLDER] :
		if not os.path.exists(folder) :
			logger.info("Create folder `%s`", folder)
			os.mkdir(folder)
	__b_createFileIfNotExists(NOTIFIERS_FILE, '{}')
	__b_createFileIfNotExists(SOURCES_FILE, '{}')


def __b_createFileIfNotExists(path: str, content: str) :
	if not os.path.exists(path) :
		logger.info("Create file `%s`", path)
		with open(path, 'w') as f :
			f.write(content)
