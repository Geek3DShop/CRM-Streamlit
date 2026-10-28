from services.backup_scheduler_service import is_backup_due
from scripts.backup import create_backup

def run_scheduled_backup(now=None):
    """Verifica se existe um backup automático pendente.Se existir, executa o backup."""
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

        return True

    except Exception as error:
        print("====================================")
        print("ERRO NO BACKUP AUTOMÁTICO")
        print("====================================")
        print(error)

        return False
    
if __name__ == "__main__":
    run_scheduled_backup()