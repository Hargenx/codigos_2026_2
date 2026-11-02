from pathlib import Path

from banco import Banco
from interface import VendaCertaApp
from negocio import Loja


def main() -> None:
    caminho = Path(__file__).resolve().parent / "dados" / "vendacerta.sqlite3"
    app = VendaCertaApp(Loja(Banco(caminho)))
    app.mainloop()


if __name__ == "__main__":
    main()
