from enum import Enum

class CustomerStatus(str, Enum):
    CONTACT = "Contato"
    POTENTIAL_CUSTOMER = "Possível cliente"
    CUSTOMER = "Cliente"
    PARTNER = "Parceiro"


class PieceStage(str, Enum):
    NOT_STARTED = "Não iniciado"
    IN_PROGRESS = "Em progresso"
    COMPLETED = "Concluído"
    LOST = "Perdido"


CRM_COLUMNS = [
    "Data",
    "Ação",
    "Status",
    "Nome",
    "Sobrenome",
    "Contato",
    "Peça",
    "Estágio da peça",
    "Valor da peça",
]