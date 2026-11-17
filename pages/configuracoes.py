import streamlit as st
from datetime import datetime

from services.backup_config_service import load_config, save_config
from services.backup_state_service import load_state
from services.backup_scheduler_service import get_scheduled_datetime

def configuracoes():
    st.title("⚙️ Configurações")

    config = load_config()
    automatic_backup = config["automatic_backup"]
    reminder = config["reminder"]
    
    # STATUS DO BACKUP
    st.subheader("📊 Status do backup")
    state = load_state()
    last_successful = state.get("last_successful_backup")
    last_error = state.get("last_error")

    # Último backup
    if last_successful:
        last_backup_datetime = datetime.fromisoformat(
            last_successful
        )
        last_backup_text = last_backup_datetime.strftime(
            "%d/%m/%Y às %H:%M"
        )
    else:
        last_backup_text = "Nenhum backup realizado"

    # Próximo backup
    if automatic_backup["enabled"]:
        next_backup = get_scheduled_datetime()

        if next_backup:
            next_backup_text = next_backup.strftime(
                "%d/%m/%Y às %H:%M"
            )
        else:
            next_backup_text = "Não definido"
    else:
        next_backup_text = "Backup automático desativado"

    # Último erro
    if last_error:
        last_error_text = last_error
    else:
        last_error_text = "Nenhum erro registrado"
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "✅ Último backup",
            last_backup_text
        )
    with col2:
        st.metric(
            "📅 Próximo backup",
            next_backup_text
        )
    with col3:
        st.metric(
            "❌ Último erro",
            last_error_text
        )

    st.divider()

    # LEMBRETE DE BACKUP
    if reminder["enabled"]:
        if last_successful:
            days_without_backup_current = (
                datetime.now() - last_backup_datetime
            ).days

            reminder_limit = int(
                reminder["days_without_backup"]
            )

            if days_without_backup_current >= reminder_limit:
                st.warning(
                    f"⚠️ O último backup foi realizado há "
                    f"{days_without_backup_current} dias."
                )

                st.info(
                    "É recomendado realizar um novo backup."
                )

        else:
            st.warning(
                "⚠️ Nenhum backup foi realizado ainda."
            )

    st.divider()
    st.subheader("💾 Backup automático")

    automatic_enabled = st.checkbox(
        "Ativar backup automático",
        value=automatic_backup["enabled"]
    )
    frequency = st.selectbox(
        "Frequência",
        ["daily", "weekly"],
        index=(
            0
            if automatic_backup["frequency"] == "daily"
            else 1
        )
    )

    if frequency == "weekly":
        days = {
            "monday": "Segunda-feira",
            "tuesday": "Terça-feira",
            "wednesday": "Quarta-feira",
            "thursday": "Quinta-feira",
            "friday": "Sexta-feira",
            "saturday": "Sábado",
            "sunday": "Domingo"
        }
        current_day = automatic_backup.get(
            "day_of_week",
            "monday"
        )
        selected_day = st.selectbox(
            "Dia da semana",
            list(days.keys()),
            index=list(days.keys()).index(current_day),
            format_func=lambda day: days[day]
        )
    else:
        selected_day = automatic_backup.get(
            "day_of_week",
            "monday"
        )

    backup_time = st.time_input(
        "Horário do backup",
        value=_parse_time(automatic_backup["time"])
    )

    st.subheader("🔔 Lembrete")
    reminder_enabled = st.checkbox(
        "Ativar lembrete",
        value=reminder["enabled"]
    )
    days_without_backup = st.number_input(
        "Mostrar lembrete após quantos dias sem backup?",
        min_value=1,
        value=int(reminder["days_without_backup"]),
        step=1
    )
    st.subheader("📁 Local do backup")

    backup_location = st.text_input(
        "Pasta onde os backups serão armazenados",
        value=config.get("backup_location", "")
    )

    if st.button("💾 Salvar configurações", type="primary"):
        new_config = {
            "automatic_backup": {
                "enabled": automatic_enabled,
                "frequency": frequency,
                "day_of_week": selected_day,
                "time": backup_time.strftime("%H:%M")
            },
            "backup_location": backup_location,
            "reminder": {
                "enabled": reminder_enabled,
                "days_without_backup": int(days_without_backup)
            }
        }
        save_config(new_config)
        st.success(
            "Configurações salvas com sucesso!"
        )

        st.rerun()

def _parse_time(value):
    hour, minute = map(int, value.split(":"))

    from datetime import time

    return time(
        hour=hour,
        minute=minute
    )
configuracoes()