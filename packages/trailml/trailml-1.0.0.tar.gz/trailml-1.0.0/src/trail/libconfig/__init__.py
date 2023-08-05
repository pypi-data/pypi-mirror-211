import os

from .config import DevelopmentConfig, ProductionConfig

if os.getenv('TRAIL_ENV') in ['dev', 'development']:
    libconfig = DevelopmentConfig
else:
    libconfig = ProductionConfig
