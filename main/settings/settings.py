import os

###########################
# ENVIRONMENT DETAILS
###########################
env_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
with open(env_file_path, 'r') as fh:
    for line in fh:
        line = line.strip()
        if line.startswith('#') or len(line.split('=')) <= 1:
            continue
        vars_dict = dict([tuple(line.split('='))])
        break

PROD = 'prod'
LOCAL = 'local'
DEPLOYMENT_ENVS = [PROD, LOCAL]

ENVIRONMENT = vars_dict.get('environment', 'local').strip()

if ENVIRONMENT not in DEPLOYMENT_ENVS:
    print(ENVIRONMENT)
    print('Invalid ENVIRONMENT in config %s' % ENVIRONMENT)
    print('VALID_ENVIRONMENTS ', DEPLOYMENT_ENVS)
    exit(-1)

if ENVIRONMENT == PROD:
    from main.settings.prod import *
elif ENVIRONMENT == LOCAL:
    from main.settings.local import *

print('Connected to ', ENVIRONMENT)
