import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from services.backup_scheduler_service import is_backup_due
from services.notification_service import (
    notify_backup_success,
    notify_backup_error
)
from scripts.backup import create_backup


def run_scheduled_backup(now=None):
    """
    Verifica se existe um backup automático pendente.
    Se existir, executa o backup.
    """

    if not is_backup_due(now):
        print("Nenhum backup automático pendente.")
        return False

    print("====================================")
    print("BACKUP AUTOMÁTICO DEVIDO")
    print("====================================")

    try:

        backup_path = create_backup("automatic")

        print("BACKUP AUTOMÁTICO REALIZADO COM SUCESSO")
        print(f"Local: {backup_path}")

        # Notificação do Windows
        notify_backup_success()

        return True

    except Exception as error:

        print("====================================")
        print("ERRO NO BACKUP AUTOMÁTICO")
        print("====================================")

        print(error)

        # Notificação de erro do Windows
        notify_backup_error(error)

        return False


if __name__ == "__main__":
    run_scheduled_backup()