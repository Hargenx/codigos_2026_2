from dataclasses import dataclass, field
from datetime import date


@dataclass(slots=True)
class Pessoa:
    cpf: str
    nome: str
    nascimento: date
    oculos: bool
    multas: list[str] = field(default_factory=list)