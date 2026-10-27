import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = PROJECT_DIR / "config" / "backup_state.json"

def load_state():
    """Carrega o estado atual do sistema de backup."""

    if not STATE_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo de estado não encontrado: {STATE_FILE}"
        )
    with STATE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def save_state(state):
    """Salva o estado atual do sistema de backup."""

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with STATE_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            state,
            file,
            indent=4,
            ensure_ascii=False
        )