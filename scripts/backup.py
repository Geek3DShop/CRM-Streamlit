from pathlib import Path
from datetime import datetime
import shutil

# CAMINHOS
PROJECT_DIR = Path(__file__).resolve().parent.parent

EXCEL_DIR = PROJECT_DIR.parent / "Excel"

BACKUP_DIR = PROJECT_DIR.parent / "Backups"

CRM_FILE = EXCEL_DIR / "CRM.xlsx"
PROFIT_LOSS_FILE = EXCEL_DIR / "CRM - Profit&Loss.xlsx"

# BACKUP
def create_backup():
    if not CRM_FILE.exists():
        raise FileNotFoundError(
            f"Tabela não encontrada: {CRM_FILE}"
        )

    if not PROFIT_LOSS_FILE.exists():
        raise FileNotFoundError(
            f"Tabela não encontrada: {PROFIT_LOSS_FILE}"
        )

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    backup_folder = BACKUP_DIR / timestamp
    backup_folder.mkdir()

    shutil.copy2(CRM_FILE, backup_folder / CRM_FILE.name)
    shutil.copy2(PROFIT_LOSS_FILE, backup_folder / PROFIT_LOSS_FILE.name)

    return backup_folder

# EXECUÇÃO DIRETA
if __name__ == "__main__":
    try:
        backup_path = create_backup()

        print("====================================")
        print("BACKUP REALIZADO COM SUCESSO")
        print("====================================")
        print(f"Local: {backup_path}")

    except Exception as error:
        print("====================================")
        print("ERRO AO REALIZAR O BACKUP")
        print("====================================")
        print(error)