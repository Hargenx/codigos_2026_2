from dataclasses import dataclass

from marca import Marca
from pessoa import Pessoa


@dataclass(slots=True)
class Veiculo:
    placa: str
    cor: str
    proprietario: Pessoa
    marca: Marca