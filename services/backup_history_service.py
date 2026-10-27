import json
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
HISTORY_FILE = PROJECT_DIR / "config" / "backup_history.json"


def load_history():
    """Carrega o histórico de backups."""

    if not HISTORY_FILE.exists():
        return []

    with HISTORY_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_history(history):
    """Salva o histórico de backups."""

    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )


def add_backup_record(
    backup_type,
    status,
    date,
    location=None,
    error=None
):
    """Adiciona uma tentativa de backup ao histórico."""

    history = load_history()

    record = {
        "date": date,
        "type": backup_type,
        "status": status,
        "location": location,
        "error": error
    }

    history.append(record)

    save_history(history)