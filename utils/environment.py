
import os

__AGENT_NAME_VAR = 'BOUQUINISTE_AGENT_NAME'

AGENT_NAME = os.environ[__AGENT_NAME_VAR] if __AGENT_NAME_VAR in os.environ else 'Bouquiniste'
