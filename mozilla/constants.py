import os


MZ_HOST = os.environ.get('MZ_HOST', '0.0.0.0')
MZ_PORT = os.environ.get('MZ_PORT', '3000')
MZ_WORKERS = int(os.environ.get('MZ_WORKERS', '1'))
MZ_DB_NAME = os.environ.get('MZ_DB_NAME', 'mozilla')
MZ_MAX_OVERDRAFT = float(os.environ.get('MZ_MAX_OVERDRAFT', '-50.00'))
