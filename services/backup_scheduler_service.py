from datetime import datetime, timedelta

from services.backup_config_service import load_config
from services.backup_state_service import load_state


def get_scheduled_datetime(now=None):
    """Retorna a data/hora do próximo backup automático."""

    if now is None:
        now = datetime.now()

    config = load_config()
    automatic_backup = config["automatic_backup"]

    if not automatic_backup["enabled"]:
        return None

    frequency = automatic_backup["frequency"]
    scheduled_time = automatic_backup["time"]

    hour, minute = map(int, scheduled_time.split(":"))

    # ==========================================
    # BACKUP DIÁRIO
    # ==========================================

    if frequency == "daily":

        scheduled = now.replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )

        if scheduled <= now:
            scheduled += timedelta(days=1)

        return scheduled

    # ==========================================
    # BACKUP SEMANAL
    # ==========================================

    if frequency == "weekly":

        days = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6
        }

        day_of_week = automatic_backup["day_of_week"].lower()

        if day_of_week not in days:
            raise ValueError(
                f"Dia da semana inválido: {day_of_week}"
            )

        target_weekday = days[day_of_week]

        days_until = (
            target_weekday - now.weekday()
        ) % 7

        scheduled = (
            now + timedelta(days=days_until)
        ).replace(
            hour=hour,
            minute=minute,
            second=0,
            microsecond=0
        )

        if scheduled <= now:
            scheduled += timedelta(days=7)

        return scheduled

    raise ValueError(
        f"Frequência não suportada: {frequency}"
    )


def get_last_successful_backup():
    """Retorna a data do último backup bem-sucedido."""

    state = load_state()

    value = state.get("last_successful_backup")

    if not value:
        return None

    return datetime.fromisoformat(value)


def is_backup_due(now=None):
    """Verifica se existe um backup automático pendente."""

    if now is None:
        now = datetime.now()

    config = load_config()
    automatic_backup = config["automatic_backup"]

    if not automatic_backup["enabled"]:
        return False

    last_backup = get_last_successful_backup()

    # ==========================================
    # PRIMEIRO BACKUP
    # ==========================================

    if last_backup is None:

        scheduled = get_scheduled_datetime(now)

        return now >= scheduled

    # ==========================================
    # PRÓXIMO BACKUP
    # ==========================================

    scheduled = get_scheduled_datetime(
        last_backup + timedelta(seconds=1)
    )

    return now >= scheduled