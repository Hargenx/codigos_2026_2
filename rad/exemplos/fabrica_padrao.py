from dataclasses import dataclass, field


@dataclass
class Pessoa:
    cpf: str
    nome: str
    multas: list[str] = field(default_factory=list)