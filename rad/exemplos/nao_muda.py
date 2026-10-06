from dataclasses import dataclass


@dataclass(frozen=True)
class Marca:
    id: int
    nome: str
    sigla: str
