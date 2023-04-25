import sys
from pathlib import Path
import os
import logging

logging.getLogger("matplotlib").setLevel(logging.WARNING)
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
