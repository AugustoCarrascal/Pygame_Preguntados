import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    RAIZ_PROYECTO = Path(sys.executable).parent
else:
    RAIZ_PROYECTO = Path(__file__).resolve().parent.parent

__all__ = ["RAIZ_PROYECTO"]
