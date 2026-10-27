from pathlib import Path
from datetime import datetime
import shutil

from services.backup_state_service import load_state, save_state
from services.backup_history_service import add_backup_record

# CAMINHOS
PROJECT_DIR = Path(__file__).resolve().parent.parent

EXCEL_DIR = PROJECT_DIR.parent / "Excel"

BACKUP_DIR = PROJECT_DIR.parent / "Backups"

CRM_FILE = EXCEL_DIR / "CRM.xlsx"
PROFIT_LOSS_FILE = EXCEL_DIR / "CRM - Profit&Loss.xlsx"

# BACKUP
def create_backup(backup_type="manual"):
    if backup_type not in ("manual", "automatic"):
        raise ValueError(
            "Tipo de backup inválido. "
            "Use 'manual' ou 'automatic'."
        )

    now = datetime.now()

    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    backup_date = now.isoformat(timespec="seconds")

    try:
       # Verifica se as tabelas existem
        if not CRM_FILE.exists():
            raise FileNotFoundError(
                f"Tabela não encontrada: {CRM_FILE}"
            )

        if not PROFIT_LOSS_FILE.exists():
            raise FileNotFoundError(
                f"Tabela não encontrada: {PROFIT_LOSS_FILE}"
            )

        # Cria a pasta principal de backups
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        
        # Cria a pasta deste backup
        backup_folder = BACKUP_DIR / timestamp
        backup_folder.mkdir()

        # Copia as duas tabelas
        shutil.copy2(
            CRM_FILE,
            backup_folder / CRM_FILE.name
        )

        shutil.copy2(
            PROFIT_LOSS_FILE,
            backup_folder / PROFIT_LOSS_FILE.name
        )

        # Registra sucesso no estado
        state = load_state()

        state["last_successful_backup"] = backup_date
        state["last_backup_type"] = backup_type
        state["last_failed_backup"] = None
        state["last_error"] = None

        save_state(state)
        
        # Registra sucesso no histórico
        add_backup_record(
            backup_type=backup_type,
            status="success",
            date=backup_date,
            location=str(backup_folder),
            error=None
        )

        return backup_folder

    except Exception as error:

        # Registra falha no estado
        state = load_state()

        state["last_failed_backup"] = backup_date
        state["last_error"] = str(error)

        save_state(state)

        # Registra falha no histórico
        add_backup_record(
            backup_type=backup_type,
            status="failed",
            date=backup_date,
            location=None,
            error=str(error)
        )

        raise



# EXECUÇÃO DIRETA
if __name__ == "__main__":
    try:
        backup_path = create_backup("manual")

        print("====================================")
        print("BACKUP REALIZADO COM SUCESSO")
        print("====================================")
        print(f"Local: {backup_path}")

    except Exception as error:
        print("====================================")
        print("ERRO AO REALIZAR O BACKUP")
        print("====================================")
        print(error)