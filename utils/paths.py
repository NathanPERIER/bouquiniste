
import os

BOUQUINISTE_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

CONFIG_FOLDER = os.path.join(BOUQUINISTE_FOLDER, 'config')

DATABASE_FILE = os.path.join(BOUQUINISTE_FOLDER, 'bouquiniste.db')
