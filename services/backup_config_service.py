import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_DIR / "config" / "backup_config.json"

def load_config():
    """Carrega as configurações de backup."""

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo de configuração não encontrado: {CONFIG_FILE}"
        )

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def save_config(config):
    """Salva as configurações de backup."""

    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            config,
            file,
            indent=4,
            ensure_ascii=False
        )