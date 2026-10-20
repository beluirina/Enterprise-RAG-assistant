import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Los tests trabajan sobre una copia de los documentos y un índice temporal,
# y nunca llaman a la API de Claude (modo extractivo).
_tmp = Path(tempfile.mkdtemp())
shutil.copytree(ROOT / "data" / "docs", _tmp / "docs")
os.environ["DOCS_DIR"] = str(_tmp / "docs")
os.environ["INDEX_DIR"] = str(_tmp / "index")
os.environ["ANTHROPIC_API_KEY"] = ""
os.environ["EMBEDDING_BACKEND"] = "tfidf"
