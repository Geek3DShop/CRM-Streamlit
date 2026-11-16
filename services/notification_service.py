from winotify import Notification
APP_ID = "CRM Geek 3D Shop"

def show_notification(title, message):
    """Exibe uma notificação do Windows."""
    toast = Notification(
        app_id=APP_ID,
        title=title,
        msg=message,
        duration="short"
    )
    toast.show()

def notify_backup_success():
    """Notifica que o backup foi realizado com sucesso."""

    show_notification(
        "Backup realizado",
        "O backup automático do CRM foi concluído com sucesso."
    )

def notify_backup_error(error):
    """Notifica que ocorreu um erro no backup."""

    show_notification(
        "Erro no backup",
        f"Não foi possível realizar o backup: {error}"
    )