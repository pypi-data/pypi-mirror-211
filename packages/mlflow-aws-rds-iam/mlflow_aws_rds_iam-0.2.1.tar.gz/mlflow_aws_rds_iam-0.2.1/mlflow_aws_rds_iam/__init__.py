import logging
import os
from importlib import metadata

logging.basicConfig(
    level=os.getenv("MLFLOW_AWS_RDS_IAM_DEBUG", "False").lower() in ("true", "1")
    or logging.INFO
)

__version__ = metadata.version(__package__)
